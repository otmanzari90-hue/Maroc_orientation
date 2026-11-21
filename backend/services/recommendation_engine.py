
import re


def normalize_words(text):
    if not text:
        return set()

    words = re.findall(r"[a-zA-ZÀ-ÿ0-9]+", str(text).lower())

    # Retirer les mots trop courts
    return {word for word in words if len(word) > 2}


def calculate_compatibility(student, program):
    """
    Score indicatif de compatibilité basé sur les intérêts
    et le projet professionnel.

    Ce score n'est pas une probabilité d'admission.
    """

    interests = set()

    for interest in student.interests:
        interests.update(normalize_words(interest))

    career_words = normalize_words(student.career_goal)

    program_words = normalize_words(
        program.get("name", "") + " " +
        program.get("keywords", "") + " " +
        program.get("career_fields", "")
    )

    interest_score = 0
    career_score = 0
    has_interests = bool(interests)
    has_career_goal = bool(career_words)

    if has_interests:
        interest_score = (
            len(interests & program_words) / len(interests)
        ) * 100

    if has_career_goal:
        career_score = (
            len(career_words & program_words) / len(career_words)
        ) * 100

    if has_interests and has_career_goal:
        score = 0.7 * interest_score + 0.3 * career_score
    elif has_interests:
        score = interest_score
    elif has_career_goal:
        score = career_score
    else:
        return None

    return round(score, 1)


def recommend_programs(student, programs, academic_year):
    from backend.services.eligibility_engine import evaluate_eligibility

    recommendations = []

    for program in programs:
        compatibility = calculate_compatibility(student, program)

        eligibility = evaluate_eligibility(
            student,
            program,
            academic_year
        )

        recommendations.append({
            "program": program,
            "compatibility_score": compatibility,
            "eligibility": eligibility
        })

    recommendations.sort(
        key=lambda item: (
            item["compatibility_score"] is not None,
            item["compatibility_score"] or 0
        ),
        reverse=True
    )

    return recommendations
