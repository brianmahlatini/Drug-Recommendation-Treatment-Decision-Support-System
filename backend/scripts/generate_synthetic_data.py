from __future__ import annotations

import csv
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RANDOM_SEED = 42

MEDICINES = [
    {
        "medicine_id": "MED-AMOX",
        "medicine_name": "Amoxicillin",
        "drug_class": "Penicillin antibiotic",
        "route": "oral",
        "diagnoses": "bacterial_sinusitis;otitis_media;community_acquired_pneumonia",
        "symptoms": "fever;productive_cough;sinus_pain;ear_pain",
        "mechanism": "beta lactam bacterial cell wall synthesis inhibitor",
        "contraindications": "penicillin_allergy",
        "interaction_groups": "anticoagulant",
        "allergy_terms": "penicillin;amoxicillin;beta_lactam",
        "min_age": 0,
        "first_line": True,
        "evidence_level": "guideline-supported first-line option for selected bacterial infections",
    },
    {
        "medicine_id": "MED-AZITH",
        "medicine_name": "Azithromycin",
        "drug_class": "Macrolide antibiotic",
        "route": "oral",
        "diagnoses": "community_acquired_pneumonia;atypical_pneumonia",
        "symptoms": "fever;dry_cough;productive_cough;shortness_of_breath",
        "mechanism": "protein synthesis inhibitor with atypical respiratory coverage",
        "contraindications": "qt_prolongation;liver_disease",
        "interaction_groups": "antiarrhythmic;warfarin",
        "allergy_terms": "macrolide;azithromycin",
        "min_age": 0,
        "first_line": False,
        "evidence_level": "guideline-supported in selected pneumonia scenarios",
    },
    {
        "medicine_id": "MED-METF",
        "medicine_name": "Metformin",
        "drug_class": "Biguanide antihyperglycemic",
        "route": "oral",
        "diagnoses": "type_2_diabetes",
        "symptoms": "polyuria;polydipsia;fatigue;elevated_glucose",
        "mechanism": "reduces hepatic glucose production and improves insulin sensitivity",
        "contraindications": "severe_renal_impairment;metabolic_acidosis",
        "interaction_groups": "renal_monitoring;contrast_media",
        "allergy_terms": "metformin",
        "min_age": 10,
        "first_line": True,
        "evidence_level": "guideline-supported first-line option for type 2 diabetes",
    },
    {
        "medicine_id": "MED-LISI",
        "medicine_name": "Lisinopril",
        "drug_class": "ACE inhibitor",
        "route": "oral",
        "diagnoses": "hypertension;heart_failure;diabetic_kidney_disease",
        "symptoms": "elevated_blood_pressure;proteinuria;edema",
        "mechanism": "angiotensin converting enzyme inhibition lowers blood pressure",
        "contraindications": "pregnancy;angioedema;hyperkalemia",
        "interaction_groups": "potassium_sparing_diuretic;lithium;renal_monitoring",
        "allergy_terms": "ace_inhibitor;lisinopril",
        "min_age": 6,
        "first_line": True,
        "evidence_level": "guideline-supported first-line option for hypertension in many adults",
    },
    {
        "medicine_id": "MED-AMLO",
        "medicine_name": "Amlodipine",
        "drug_class": "Calcium channel blocker",
        "route": "oral",
        "diagnoses": "hypertension;stable_angina",
        "symptoms": "elevated_blood_pressure;chest_discomfort",
        "mechanism": "dihydropyridine calcium channel blockade causes vasodilation",
        "contraindications": "severe_hypotension",
        "interaction_groups": "cyp3a4_inhibitor",
        "allergy_terms": "amlodipine",
        "min_age": 6,
        "first_line": True,
        "evidence_level": "guideline-supported first-line option for hypertension",
    },
    {
        "medicine_id": "MED-ALB",
        "medicine_name": "Albuterol inhaler",
        "drug_class": "Short-acting beta agonist",
        "route": "inhaled",
        "diagnoses": "asthma;copd_exacerbation",
        "symptoms": "wheezing;shortness_of_breath;chest_tightness;cough",
        "mechanism": "bronchodilation through beta 2 adrenergic receptor agonism",
        "contraindications": "tachyarrhythmia",
        "interaction_groups": "beta_blocker",
        "allergy_terms": "albuterol;salbutamol",
        "min_age": 4,
        "first_line": True,
        "evidence_level": "rescue therapy standard for bronchospasm",
    },
    {
        "medicine_id": "MED-BUD",
        "medicine_name": "Budesonide inhaler",
        "drug_class": "Inhaled corticosteroid",
        "route": "inhaled",
        "diagnoses": "asthma",
        "symptoms": "wheezing;night_cough;shortness_of_breath;chest_tightness",
        "mechanism": "local airway anti inflammatory controller therapy",
        "contraindications": "untreated_systemic_infection",
        "interaction_groups": "cyp3a4_inhibitor",
        "allergy_terms": "budesonide;corticosteroid",
        "min_age": 6,
        "first_line": True,
        "evidence_level": "guideline-supported controller therapy for persistent asthma",
    },
    {
        "medicine_id": "MED-IBU",
        "medicine_name": "Ibuprofen",
        "drug_class": "NSAID",
        "route": "oral",
        "diagnoses": "musculoskeletal_pain;osteoarthritis;fever",
        "symptoms": "pain;inflammation;fever;joint_pain",
        "mechanism": "cyclooxygenase inhibition reduces prostaglandin synthesis",
        "contraindications": "peptic_ulcer;severe_renal_impairment;nsaid_allergy;third_trimester_pregnancy",
        "interaction_groups": "anticoagulant;antiplatelet;nsaid;renal_monitoring",
        "allergy_terms": "nsaid;ibuprofen;aspirin",
        "min_age": 6,
        "first_line": False,
        "evidence_level": "common symptomatic therapy with safety restrictions",
    },
    {
        "medicine_id": "MED-ACET",
        "medicine_name": "Acetaminophen",
        "drug_class": "Analgesic antipyretic",
        "route": "oral",
        "diagnoses": "musculoskeletal_pain;fever;osteoarthritis",
        "symptoms": "pain;fever;headache;joint_pain",
        "mechanism": "central analgesic and antipyretic effect",
        "contraindications": "severe_liver_disease",
        "interaction_groups": "warfarin;liver_monitoring",
        "allergy_terms": "acetaminophen;paracetamol",
        "min_age": 0,
        "first_line": True,
        "evidence_level": "common first-line symptomatic therapy when dosed safely",
    },
    {
        "medicine_id": "MED-OMEP",
        "medicine_name": "Omeprazole",
        "drug_class": "Proton pump inhibitor",
        "route": "oral",
        "diagnoses": "gerd;peptic_ulcer_disease",
        "symptoms": "heartburn;reflux;epigastric_pain;nausea",
        "mechanism": "gastric proton pump inhibition reduces acid secretion",
        "contraindications": "rilpivirine_use",
        "interaction_groups": "clopidogrel;magnesium_monitoring",
        "allergy_terms": "omeprazole;ppi",
        "min_age": 1,
        "first_line": True,
        "evidence_level": "guideline-supported acid suppression for GERD and ulcers",
    },
    {
        "medicine_id": "MED-SER",
        "medicine_name": "Sertraline",
        "drug_class": "SSRI antidepressant",
        "route": "oral",
        "diagnoses": "major_depressive_disorder;generalized_anxiety_disorder",
        "symptoms": "low_mood;anxiety;insomnia;loss_of_interest",
        "mechanism": "selective serotonin reuptake inhibition",
        "contraindications": "maoi_use",
        "interaction_groups": "ssri;anticoagulant;triptan",
        "allergy_terms": "sertraline;ssri",
        "min_age": 6,
        "first_line": True,
        "evidence_level": "guideline-supported first-line option for depression and anxiety",
    },
    {
        "medicine_id": "MED-LORA",
        "medicine_name": "Loratadine",
        "drug_class": "Second-generation antihistamine",
        "route": "oral",
        "diagnoses": "allergic_rhinitis;urticaria",
        "symptoms": "sneezing;itching;runny_nose;hives",
        "mechanism": "histamine H1 receptor antagonism",
        "contraindications": "severe_liver_disease",
        "interaction_groups": "cyp3a4_inhibitor",
        "allergy_terms": "loratadine;antihistamine",
        "min_age": 2,
        "first_line": True,
        "evidence_level": "guideline-supported symptomatic option for allergic rhinitis",
    },
]


def write_medicines() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "medicines.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(MEDICINES[0].keys()))
        writer.writeheader()
        writer.writerows(MEDICINES)


def write_cases() -> None:
    random.seed(RANDOM_SEED)
    path = DATA_DIR / "treatment_cases.csv"
    fieldnames = [
        "case_id",
        "age",
        "sex",
        "diagnosis",
        "symptoms",
        "medicine_id",
        "severity",
        "outcome",
        "adverse_event",
    ]
    sexes = ["female", "male", "unknown"]
    severities = ["mild", "moderate", "severe"]
    outcomes = ["resolved", "improved", "unchanged", "adverse_event"]

    rows = []
    for index in range(420):
        med = random.choice(MEDICINES)
        diagnosis = random.choice(med["diagnoses"].split(";"))
        symptoms = random.sample(med["symptoms"].split(";"), k=min(3, len(med["symptoms"].split(";"))))
        first_line_bonus = 0.14 if med["first_line"] else 0.0
        success_probability = 0.62 + first_line_bonus - (0.10 if random.choice(severities) == "severe" else 0.0)
        outcome = random.choices(outcomes, weights=[success_probability, 0.22, 0.12, 0.04], k=1)[0]
        rows.append(
            {
                "case_id": f"CASE-{index + 1:04d}",
                "age": random.randint(max(0, int(med["min_age"])), 88),
                "sex": random.choice(sexes),
                "diagnosis": diagnosis,
                "symptoms": ";".join(symptoms),
                "medicine_id": med["medicine_id"],
                "severity": random.choice(severities),
                "outcome": outcome,
                "adverse_event": "none" if outcome != "adverse_event" else random.choice(["rash", "gi_upset", "dizziness"]),
            }
        )

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    write_medicines()
    write_cases()
    print(f"Synthetic clinical prototype data written to {DATA_DIR}")

