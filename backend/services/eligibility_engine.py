
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

RULES_FILE = (
    BASE_DIR / "data" / "admission_rules" / "admission_rules.csv"
)


def load_admission_rules():
    if not RULES_FILE.exists():
        return []

    df = pd.read_csv(RULES_FILE, dtype=str).fillna("")
    return df.to_dict(orient="records")


def normalize(value):
    return " ".join(str(value).lower().strip().split())


def evaluate_eligibility(student, program, academic_year):
    """
    Évalue l'éligibilité à partir des règles enregistrées.
    Ne prédit pas les chances réelles d'admission.
    """

    rules = load_admission_rules()

    matching_rules = [
        rule for rule in rules
        if rule["program_id"] == program.get("program_id")
        and rule["academic_year"] == academic_year
    ]

    if not matching_rules:
        return {
            "status": "insufficient_information",
            "reason": "Aucune règle vérifiée disponible pour cette année."
        }

    rule = matching_rules[0]

    if not rule["official_url"] or not rule["source_verified_at"]:
        return {
            "status": "insufficient_information",
            "reason": "La source officielle ou sa date de vérification manque."
        }

    accepted_streams = [
        normalize(stream)
        for stream in rule["accepted_bac_streams"].split(";")
        if stream.strip()
    ]

    if not accepted_streams:
        return {
            "status": "insufficient_information",
            "reason": "Les séries du Bac acceptées ne sont pas renseignées."
        }

    student_stream = normalize(student.bac_stream)

    if student_stream not in accepted_streams:
        return {
            "status": "not_eligible",
            "reason": "La série du Bac ne figure pas parmi les séries acceptées."
        }

    minimum_grade = rule["min_general_average"]

    if minimum_grade:
        if student.general_average is None:
            return {
                "status": "insufficient_information",
                "reason": "La moyenne générale de l'étudiant est nécessaire."
            }

        if student.general_average < float(minimum_grade):
            return {
                "status": "not_eligible",
                "reason": f"Moyenne minimale requise : {minimum_grade}/20."
            }

    return {
        "status": "eligible_based_on_recorded_criteria",
        "reason": "Les critères renseignés dans la règle sont satisfaits.",
        "selection_method": rule["selection_method"],
        "source": rule["official_url"],
        "verified_at": rule["source_verified_at"]
    }
