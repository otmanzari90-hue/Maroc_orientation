from backend.api.orientations import router as orientations_router
from fastapi import FastAPI

from backend.api.programs import router as programs_router
from backend.api.students import router as students_router

from backend.database.database import Base, engine
from backend.database import models

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Moroccan Bac AI",
    description="Plateforme intelligente d'orientation post-Bac au Maroc",
    version="0.3.0"
)


@app.get("/")
def home():
    return {
        "project": "Moroccan Bac AI",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(programs_router)
app.include_router(students_router)
app.include_router(orientations_router)