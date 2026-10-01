from requirement_extractor import (
    extract_job_requirements,
    extract_resume_terms,
    normalize_term
)


def analyze_skill_gap(resume_text, job_description):
    """
    Analyze matching and missing skills/requirements.

    Uses both:
    1. Structured skills from skills.csv
    2. Dynamically detected professional requirements
    """

    resume_terms = extract_resume_terms(resume_text)

    job_data = extract_job_requirements(job_description)

    job_requirements = job_data["all_requirements"]

    # Create normalized lookup dictionaries
    resume_lookup = {
        normalize_term(term): term
        for term in resume_terms
    }

    job_lookup = {
        normalize_term(term): term
        for term in job_requirements
    }

    matching_normalized = (
        set(resume_lookup.keys())
        &
        set(job_lookup.keys())
    )

    missing_normalized = (
        set(job_lookup.keys())
        -
        set(resume_lookup.keys())
    )

    additional_normalized = (
        set(resume_lookup.keys())
        -
        set(job_lookup.keys())
    )

    matching_skills = sorted(
        [
            job_lookup[item]
            for item in matching_normalized
        ],
        key=str.lower
    )

    missing_skills = sorted(
        [
            job_lookup[item]
            for item in missing_normalized
        ],
        key=str.lower
    )

    additional_skills = sorted(
        [
            resume_lookup[item]
            for item in additional_normalized
        ],
        key=str.lower
    )

    if len(job_requirements) > 0:

        skill_match_percentage = (
            len(matching_skills)
            /
            len(job_requirements)
        ) * 100

    else:

        skill_match_percentage = 0

    return {
        "resume_skills": sorted(
            resume_terms,
            key=str.lower
        ),

        "job_skills": sorted(
            job_requirements,
            key=str.lower
        ),

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "additional_skills": additional_skills,

        "skill_match_percentage": round(
            skill_match_percentage,
            2
        ),

        "known_job_skills": job_data[
            "known_skills"
        ],

        "dynamic_job_requirements": job_data[
            "dynamic_requirements"
        ]
    }