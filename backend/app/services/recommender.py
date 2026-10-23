from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.ml.outcome_model import OutcomePredictionModel
from app.schemas.clinical import ClinicalProfile, Recommendation, RecommendationResponse
from app.services.safety import SafetyContext, evaluate_safety, normalize_terms

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DISCLAIMER = (
    "Clinical decision-support prototype only. Recommendations require clinician review, "
    "local guideline alignment, and patient-specific verification before use."
)


def split_terms(value: str) -> set[str]:
    if pd.isna(value) or not str(value).strip():
        return set()
    return {item.strip().lower().replace(" ", "_") for item in str(value).split(";") if item.strip()}


def to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


@dataclass
class LoadedData:
    medicines: pd.DataFrame
    cases: pd.DataFrame


class RecommendationEngine:
    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        self.data_dir = data_dir
        self.loaded = self._load_data()
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.medicine_matrix = self.vectorizer.fit_transform(self.loaded.medicines["search_text"])
        self.outcome_priors = self._build_outcome_priors()
        self.outcome_model = OutcomePredictionModel.load()

    def _load_data(self) -> LoadedData:
        medicines_path = self.data_dir / "medicines.csv"
        cases_path = self.data_dir / "treatment_cases.csv"
        if not medicines_path.exists() or not cases_path.exists():
            raise RuntimeError("Dataset files are missing. Run backend/scripts/generate_synthetic_data.py first.")

        medicines = pd.read_csv(medicines_path)
        cases = pd.read_csv(cases_path)
        medicines["search_text"] = (
            medicines["diagnoses"].fillna("")
            + " "
            + medicines["symptoms"].fillna("")
            + " "
            + medicines["drug_class"].fillna("")
            + " "
            + medicines["mechanism"].fillna("")
        )
        return LoadedData(medicines=medicines, cases=cases)

    def _build_outcome_priors(self) -> dict[str, float]:
        cases = self.loaded.cases.copy()
        if cases.empty:
            return {}
        cases["success"] = cases["outcome"].isin(["improved", "resolved"]).astype(float)
        grouped = cases.groupby("medicine_id")["success"].mean()
        return grouped.to_dict()

    def metadata(self) -> dict[str, list[str]]:
        medicines = self.loaded.medicines
        diagnoses = sorted({term.replace("_", " ") for value in medicines["diagnoses"] for term in split_terms(value)})
        symptoms = sorted({term.replace("_", " ") for value in medicines["symptoms"] for term in split_terms(value)})
        comorbidities = sorted(
            {
                term.replace("_", " ")
                for value in medicines["contraindications"]
                for term in split_terms(value)
                if term not in {"pregnancy"}
            }
        )
        medicines_list = sorted(medicines["medicine_name"].tolist())
        return {
            "diagnoses": diagnoses,
            "symptoms": symptoms,
            "comorbidities": comorbidities,
            "medicines": medicines_list,
            "allergies": ["penicillin", "sulfonamide", "nsaid", "ace inhibitor", "macrolide"],
        }

    def recommend(self, profile: ClinicalProfile, limit: int = 6) -> RecommendationResponse:
        query = self._profile_to_query(profile)
        query_matrix = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_matrix, self.medicine_matrix).flatten()

        scored_rows = []
        for index, row in self.loaded.medicines.iterrows():
            clinical_score = float(similarities[index])
            rule_score = self._rule_score(profile, row)
            outcome_score = self.outcome_priors.get(row["medicine_id"], 0.55)
            ml_success_probability = self._ml_success_probability(profile, row, outcome_score)
            total_score = (
                (0.40 * ml_success_probability)
                + (0.30 * clinical_score)
                + (0.20 * rule_score)
                + (0.10 * outcome_score)
            )
            scored_rows.append((total_score, clinical_score, rule_score, outcome_score, ml_success_probability, row))

        ranked = sorted(scored_rows, key=lambda item: item[0], reverse=True)
        recommendations = [self._to_recommendation(profile, *item) for item in ranked[:limit]]
        recommendations.sort(key=lambda item: (item.recommendation_status == "blocked", -item.score))

        return RecommendationResponse(
            disclaimer=DISCLAIMER,
            profile_summary=self._summary(profile),
            recommendations=recommendations,
        )

    def _profile_to_query(self, profile: ClinicalProfile) -> str:
        values = [profile.diagnosis, profile.severity, *profile.symptoms, *profile.comorbidities]
        return " ".join(value.lower().replace(" ", "_") for value in values if value)

    def _rule_score(self, profile: ClinicalProfile, row: pd.Series) -> float:
        diagnosis = profile.diagnosis.lower().replace(" ", "_")
        symptoms = normalize_terms(profile.symptoms)
        indicated_diagnoses = split_terms(row["diagnoses"])
        indicated_symptoms = split_terms(row["symptoms"])

        score = 0.0
        if diagnosis in indicated_diagnoses:
            score += 0.55
        if symptoms:
            score += 0.30 * (len(symptoms.intersection(indicated_symptoms)) / max(len(symptoms), 1))
        if to_bool(row["first_line"]):
            score += 0.15
        return min(score, 1.0)

    def _ml_success_probability(self, profile: ClinicalProfile, row: pd.Series, fallback_score: float) -> float:
        if self.outcome_model is None:
            return float(fallback_score)
        return self.outcome_model.predict_success_probability(profile, row)

    def _to_recommendation(
        self,
        profile: ClinicalProfile,
        total_score: float,
        clinical_score: float,
        rule_score: float,
        outcome_score: float,
        ml_success_probability: float,
        row: pd.Series,
    ) -> Recommendation:
        context = SafetyContext(
            medicine_name=row["medicine_name"],
            drug_class=row["drug_class"],
            contraindications=split_terms(row["contraindications"]),
            interaction_groups=split_terms(row["interaction_groups"]),
            min_age=int(row["min_age"]),
            allergy_terms=split_terms(row["allergy_terms"]),
        )
        safety_issues = evaluate_safety(profile, context)
        has_block = any(issue.severity == "block" for issue in safety_issues)
        has_warning = any(issue.severity == "warning" for issue in safety_issues)
        adjusted_score = max(0.0, total_score - (0.45 if has_block else 0.0) - (0.10 if has_warning else 0.0))

        if adjusted_score >= 0.70 and not has_block:
            confidence = "high"
        elif adjusted_score >= 0.42 and not has_block:
            confidence = "moderate"
        else:
            confidence = "low"

        status = "blocked" if has_block else "use_with_caution" if has_warning else "candidate"
        explanation = [
            f"Supervised ML predicted success probability {ml_success_probability:.2f}.",
            f"Matched diagnosis/symptom profile with content similarity {clinical_score:.2f}.",
            f"Rule alignment score {rule_score:.2f} based on indication, symptoms, and first-line status.",
            f"Synthetic outcome prior {outcome_score:.2f} from generated treatment cases.",
            f"Evidence tier: {row['evidence_level']}.",
        ]

        return Recommendation(
            medicine_id=row["medicine_id"],
            medicine_name=row["medicine_name"],
            drug_class=row["drug_class"],
            route=row["route"],
            score=round(adjusted_score, 3),
            ml_success_probability=round(ml_success_probability, 3),
            confidence=confidence,
            evidence_level=row["evidence_level"],
            recommendation_status=status,
            explanation=explanation,
            safety_issues=safety_issues,
        )

    def _summary(self, profile: ClinicalProfile) -> str:
        symptom_text = ", ".join(profile.symptoms) if profile.symptoms else "no symptoms recorded"
        return f"{profile.age} year-old {profile.sex} patient with {profile.diagnosis}; symptoms: {symptom_text}."


recommendation_engine = RecommendationEngine()

