from __future__ import annotations

from dataclasses import dataclass

from app.schemas.clinical import ClinicalProfile, SafetyIssue


@dataclass(frozen=True)
class SafetyContext:
    medicine_name: str
    drug_class: str
    contraindications: set[str]
    interaction_groups: set[str]
    min_age: int
    allergy_terms: set[str]


NORMALIZED_INTERACTIONS = {
    "warfarin": "anticoagulant",
    "apixaban": "anticoagulant",
    "rivaroxaban": "anticoagulant",
    "insulin": "hypoglycemic",
    "glipizide": "hypoglycemic",
    "lithium": "lithium",
    "sertraline": "ssri",
    "fluoxetine": "ssri",
    "ibuprofen": "nsaid",
    "naproxen": "nsaid",
    "aspirin": "antiplatelet",
    "clopidogrel": "antiplatelet",
}


def normalize_terms(values: list[str] | set[str]) -> set[str]:
    return {value.strip().lower().replace(" ", "_") for value in values if value.strip()}


def evaluate_safety(profile: ClinicalProfile, context: SafetyContext) -> list[SafetyIssue]:
    issues: list[SafetyIssue] = []
    allergies = normalize_terms(profile.allergies)
    comorbidities = normalize_terms(profile.comorbidities)
    current_meds = normalize_terms(profile.current_medications)
    current_groups = {NORMALIZED_INTERACTIONS.get(med, med) for med in current_meds}

    allergy_hits = allergies.intersection(context.allergy_terms | {context.drug_class.lower().replace(" ", "_")})
    for allergy in sorted(allergy_hits):
        issues.append(
            SafetyIssue(
                severity="block",
                category="allergy",
                message=f"Recorded allergy may apply to {context.medicine_name}: {allergy.replace('_', ' ')}.",
            )
        )

    contraindication_hits = comorbidities.intersection(context.contraindications)
    if profile.pregnant and "pregnancy" in context.contraindications:
        contraindication_hits.add("pregnancy")

    for condition in sorted(contraindication_hits):
        issues.append(
            SafetyIssue(
                severity="block",
                category="contraindication",
                message=f"{context.medicine_name} is contraindicated or not preferred with {condition.replace('_', ' ')}.",
            )
        )

    if profile.age < context.min_age:
        issues.append(
            SafetyIssue(
                severity="block",
                category="age",
                message=f"{context.medicine_name} is configured for patients age {context.min_age}+ in this prototype.",
            )
        )

    interaction_hits = current_groups.intersection(context.interaction_groups)
    for interaction in sorted(interaction_hits):
        issues.append(
            SafetyIssue(
                severity="warning",
                category="interaction",
                message=f"Potential interaction risk with current {interaction.replace('_', ' ')} therapy.",
            )
        )

    if "renal_impairment" in comorbidities and "renal_monitoring" in context.interaction_groups:
        issues.append(
            SafetyIssue(
                severity="monitor",
                category="monitoring",
                message=f"Renal dosing and kidney-function monitoring are recommended for {context.medicine_name}.",
            )
        )

    if profile.severity == "severe":
        issues.append(
            SafetyIssue(
                severity="monitor",
                category="acuity",
                message="Severe presentations require urgent clinician assessment before treatment selection.",
            )
        )

    return issues

