
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON

from backend.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(50), nullable=False)
    bac_stream = Column(String(100), nullable=False)

    regional_grade = Column(Float, nullable=True)
    national_grade = Column(Float, nullable=True)
    general_average = Column(Float, nullable=True)

    city = Column(String(100), nullable=True)

    interests = Column(JSON, nullable=False, default=list)

    career_goal = Column(String(200), nullable=True)
    preferred_language = Column(String(10), default="fr")

    created_at = Column(DateTime, default=datetime.utcnow)
