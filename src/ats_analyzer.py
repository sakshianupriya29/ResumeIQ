from requirement_extractor import (
    extract_job_requirements,
    extract_resume_terms,
    normalize_term
)


def analyze_ats_keywords(resume_text, job_description):
    """
    Analyze ATS-style keyword coverage using both
    structured skills and dynamically detected requirements.

    This is an ATS-style analysis and not a proprietary
    ATS score.
    """

    resume_terms = extract_resume_terms(
        resume_text
    )

    job_data = extract_job_requirements(
        job_description
    )

    job_requirements = job_data[
        "all_requirements"
    ]

    resume_lookup = {
        normalize_term(term): term
        for term in resume_terms
    }

    job_lookup = {
        normalize_term(term): term
        for term in job_requirements
    }

    matched_normalized = (
        set(resume_lookup.keys())
        &
        set(job_lookup.keys())
    )

    missing_normalized = (
        set(job_lookup.keys())
        -
        set(resume_lookup.keys())
    )

    matched_keywords = sorted(
        [
            job_lookup[item]
            for item in matched_normalized
        ],
        key=str.lower
    )

    missing_keywords = sorted(
        [
            job_lookup[item]
            for item in missing_normalized
        ],
        key=str.lower
    )

    total_keywords = len(job_requirements)

    if total_keywords > 0:

        keyword_coverage = (
            len(matched_keywords)
            /
            total_keywords
        ) * 100

    else:

        keyword_coverage = 0

    return {
        "total_keywords": total_keywords,

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,

        "keyword_coverage": round(
            keyword_coverage,
            2
        ),

        "known_keywords": job_data[
            "known_skills"
        ],

        "dynamic_keywords": job_data[
            "dynamic_requirements"
        ]
    }