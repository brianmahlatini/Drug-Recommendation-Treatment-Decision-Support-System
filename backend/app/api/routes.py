from fastapi import APIRouter

from app.schemas.clinical import ClinicalProfile, RecommendationResponse
from app.services.recommender import recommendation_engine

router = APIRouter()


@router.get("/metadata", tags=["clinical"])
def metadata() -> dict[str, list[str]]:
    return recommendation_engine.metadata()


@router.post("/recommendations", response_model=RecommendationResponse, tags=["clinical"])
def recommendations(profile: ClinicalProfile) -> RecommendationResponse:
    return recommendation_engine.recommend(profile)

