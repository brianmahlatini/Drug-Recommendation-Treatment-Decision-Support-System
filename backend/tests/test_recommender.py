from app.schemas.clinical import ClinicalProfile
from app.services.recommender import RecommendationEngine


def test_recommender_returns_ranked_candidates() -> None:
    engine = RecommendationEngine()
    profile = ClinicalProfile(
        age=52,
        sex="female",
        diagnosis="type 2 diabetes",
        symptoms=["elevated glucose", "fatigue"],
        comorbidities=[],
    )

    response = engine.recommend(profile)

    assert response.recommendations
    assert response.recommendations[0].score >= response.recommendations[-1].score
    assert 0 <= response.recommendations[0].ml_success_probability <= 1
    assert any("Supervised ML predicted success probability" in item for item in response.recommendations[0].explanation)

