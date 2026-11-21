
from pathlib import Path
import pandas as pd

# Chemin vers le dossier principal du projet
BASE_DIR = Path(__file__).resolve().parents[2]

PROGRAMS_FILE = BASE_DIR / "data" / "programs" / "programs.csv"


def get_all_programs():
    """Récupère toutes les formations du catalogue."""

    if not PROGRAMS_FILE.exists():
        return []

    df = pd.read_csv(PROGRAMS_FILE, dtype=str).fillna("")

    return df.to_dict(orient="records")


def search_programs(query=None, city=None):
    """Recherche des formations par nom, ville ou filière du Bac."""

    programs = get_all_programs()

    results = []

    for program in programs:
        searchable_text = (
            program["name"] + " " +
            program["city"] + " " +
            program["bac_streams"]
        ).lower()

        if query and query.lower() not in searchable_text:
            continue

        if city and city.lower() not in program["city"].lower():
            continue

        results.append(program)

    return results
