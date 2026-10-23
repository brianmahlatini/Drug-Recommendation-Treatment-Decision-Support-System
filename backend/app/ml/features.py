from __future__ import annotations

from typing import Any

import pandas as pd

from app.schemas.clinical import ClinicalProfile


SUCCESS_OUTCOMES = {"improved", "resolved"}


def split_terms(value: Any) -> set[str]:
    if pd.isna(value) or not str(value).strip():
        return set()
    return {item.strip().lower().replace(" ", "_") for item in str(value).split(";") if item.strip()}


def normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def symptom_match_ratio(patient_symptoms: set[str], medicine_symptoms: set[str]) -> float:
    if not patient_symptoms:
        return 0.0
    return len(patient_symptoms.intersection(medicine_symptoms)) / len(patient_symptoms)


def make_training_frame(cases: pd.DataFrame, medicines: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    medicine_features = medicines[
        [
            "medicine_id",
            "drug_class",
            "route",
            "diagnoses",
            "symptoms",
            "min_age",
            "first_line",
        ]
    ].copy()
    frame = cases.merge(medicine_features, on="medicine_id", how="left", suffixes=("_case", "_medicine"))

    rows: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        case_symptoms = split_terms(row["symptoms_case"])
        medicine_symptoms = split_terms(row["symptoms_medicine"])
        medicine_diagnoses = split_terms(row["diagnoses"])
        diagnosis = normalize(str(row["diagnosis"]))
        min_age = int(row["min_age"])
        age = int(row["age"])

        rows.append(
            {
                "age": age,
                "sex": str(row["sex"]),
                "diagnosis": diagnosis,
                "severity": str(row["severity"]),
                "medicine_id": str(row["medicine_id"]),
                "drug_class": str(row["drug_class"]),
                "route": str(row["route"]),
                "first_line": int(to_bool(row["first_line"])),
                "min_age": min_age,
                "age_below_minimum": int(age < min_age),
                "diagnosis_match": int(diagnosis in medicine_diagnoses),
                "symptom_match_ratio": symptom_match_ratio(case_symptoms, medicine_symptoms),
                "symptom_count": len(case_symptoms),
                "comorbidity_count": 0,
                "allergy_count": 0,
                "current_medication_count": 0,
                "pregnant": 0,
            }
        )

    target = frame["outcome"].isin(SUCCESS_OUTCOMES).astype(int)
    return pd.DataFrame(rows), target


def make_prediction_frame(profile: ClinicalProfile, medicine: pd.Series) -> pd.DataFrame:
    diagnosis = normalize(profile.diagnosis)
    patient_symptoms = {normalize(symptom) for symptom in profile.symptoms}
    medicine_symptoms = split_terms(medicine["symptoms"])
    medicine_diagnoses = split_terms(medicine["diagnoses"])
    min_age = int(medicine["min_age"])

    return pd.DataFrame(
        [
            {
                "age": int(profile.age),
                "sex": profile.sex,
                "diagnosis": diagnosis,
                "severity": profile.severity,
                "medicine_id": str(medicine["medicine_id"]),
                "drug_class": str(medicine["drug_class"]),
                "route": str(medicine["route"]),
                "first_line": int(to_bool(medicine["first_line"])),
                "min_age": min_age,
                "age_below_minimum": int(profile.age < min_age),
                "diagnosis_match": int(diagnosis in medicine_diagnoses),
                "symptom_match_ratio": symptom_match_ratio(patient_symptoms, medicine_symptoms),
                "symptom_count": len(patient_symptoms),
                "comorbidity_count": len(profile.comorbidities),
                "allergy_count": len(profile.allergies),
                "current_medication_count": len(profile.current_medications),
                "pregnant": int(profile.pregnant),
            }
        ]
    )


CATEGORICAL_FEATURES = ["sex", "diagnosis", "severity", "medicine_id", "drug_class", "route"]
NUMERIC_FEATURES = [
    "age",
    "first_line",
    "min_age",
    "age_below_minimum",
    "diagnosis_match",
    "symptom_match_ratio",
    "symptom_count",
    "comorbidity_count",
    "allergy_count",
    "current_medication_count",
    "pregnant",
]

