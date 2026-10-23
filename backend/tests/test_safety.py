from app.schemas.clinical import ClinicalProfile
from app.services.safety import SafetyContext, evaluate_safety


def test_allergy_creates_blocking_issue() -> None:
    profile = ClinicalProfile(age=35, diagnosis="bacterial sinusitis", allergies=["penicillin"])
    context = SafetyContext(
        medicine_name="Amoxicillin",
        drug_class="Penicillin antibiotic",
        contraindications={"penicillin_allergy"},
        interaction_groups=set(),
        min_age=0,
        allergy_terms={"penicillin"},
    )

    issues = evaluate_safety(profile, context)

    assert any(issue.severity == "block" and issue.category == "allergy" for issue in issues)

