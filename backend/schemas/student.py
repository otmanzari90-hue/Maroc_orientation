
from pydantic import BaseModel, Field
from typing import Optional, List


class StudentProfile(BaseModel):

    first_name: str = Field(min_length=2, max_length=50)

    bac_stream: str

    regional_grade: Optional[float] = Field(
        default=None, ge=0, le=20
    )

    national_grade: Optional[float] = Field(
        default=None, ge=0, le=20
    )

    general_average: Optional[float] = Field(
        default=None, ge=0, le=20
    )

    city: Optional[str] = None

    interests: List[str] = Field(default_factory=list)

    career_goal: Optional[str] = None

    preferred_language: str = "fr"
