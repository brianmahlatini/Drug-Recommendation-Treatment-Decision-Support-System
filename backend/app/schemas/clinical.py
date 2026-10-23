from typing import Literal

from pydantic import BaseModel, Field


Sex = Literal["female", "male", "intersex", "unknown"]
Severity = Literal["mild", "moderate", "severe"]


class ClinicalProfile(BaseModel):
    age: int = Field(ge=0, le=120)
    sex: Sex = "unknown"
    diagnosis: str = Field(min_length=2, max_length=120)
    symptoms: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    comorbidities: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)
    pregnant: bool = False
    severity: Severity = "moderate"


class SafetyIssue(BaseModel):
    severity: Literal["block", "warning", "monitor"]
    category: str
    message: str


class Recommendation(BaseModel):
    medicine_id: str
    medicine_name: str
    drug_class: str
    route: str
    score: float
    ml_success_probability: float
    confidence: Literal["low", "moderate", "high"]
    evidence_level: str
    recommendation_status: Literal["candidate", "use_with_caution", "blocked"]
    explanation: list[str]
    safety_issues: list[SafetyIssue]


class RecommendationResponse(BaseModel):
    disclaimer: str
    profile_summary: str
    recommendations: list[Recommendation]

