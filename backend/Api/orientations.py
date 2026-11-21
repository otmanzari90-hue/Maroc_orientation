
from fastapi import APIRouter, Query

from backend.schemas.student import StudentProfile
from backend.services.catalogue_service import get_all_programs
from backend.services.recommendation_engine import recommend_programs


router = APIRouter(
    prefix="/orientations",
    tags=["Orientation intelligente"]
)


@router.post("/recommend")
def get_recommendations(
    student: StudentProfile,
    academic_year: str = Query(default="2026-2027")
):
    programs = get_all_programs()

    recommendations = recommend_programs(
        student,
        programs,
        academic_year
    )

    return {
        "status": "success",
        "academic_year": academic_year,
        "total_programs": len(programs),
        "recommendations": recommendations,
        "disclaimer": (
            "Le score mesure une compatibilité indicative, "
            "pas une probabilité d'admission."
        )
    }
