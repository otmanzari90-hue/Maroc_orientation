
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Student
from backend.schemas.student import StudentProfile

router = APIRouter(
    prefix="/students",
    tags=["Profils étudiants"]
)


@router.post("/profile")
def create_student_profile(
    student: StudentProfile,
    db: Session = Depends(get_db)
):
    new_student = Student(
        **student.model_dump()
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "status": "success",
        "message": "Profil enregistré dans la base de données",
        "student_id": new_student.id,
        "student": student.model_dump()
    }


@router.get("/{student_id}")
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Étudiant introuvable"
        )

    return {
        "student": {
            "id": student.id,
            "first_name": student.first_name,
            "bac_stream": student.bac_stream,
            "regional_grade": student.regional_grade,
            "national_grade": student.national_grade,
            "general_average": student.general_average,
            "city": student.city,
            "interests": student.interests,
            "career_goal": student.career_goal,
            "preferred_language": student.preferred_language
        }
    }
