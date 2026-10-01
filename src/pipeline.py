from resume_parser import extract_text_from_pdf
from matcher import calculate_match_score
from analyzer import analyze_skill_gap
from recommendations import generate_recommendations
from ats_analyzer import analyze_ats_keywords
from resume_stats import analyze_resume_statistics


def analyze_resume_against_job(pdf_path, job_description):
    """
    Run the complete ResumeIQ analysis pipeline.

    Parameters:
        pdf_path: Path to the resume PDF
        job_description: Job description text

    Returns:
        Dictionary containing all ResumeIQ analysis results.
    """

    # --------------------------------------------------
    # 1. Extract resume text
    # --------------------------------------------------

    resume_text = extract_text_from_pdf(pdf_path)

    # --------------------------------------------------
    # 2. Calculate overall resume-job match
    # --------------------------------------------------

    match_score = calculate_match_score(
        resume_text,
        job_description
    )

    # --------------------------------------------------
    # 3. Analyze skills
    # --------------------------------------------------

    skill_analysis = analyze_skill_gap(
        resume_text,
        job_description
    )

    # --------------------------------------------------
    # 4. Generate recommendations
    # --------------------------------------------------

    recommendations = generate_recommendations(
        skill_analysis["missing_skills"],
        skill_analysis["matching_skills"],
        skill_analysis["skill_match_percentage"]
    )

    # --------------------------------------------------
    # 5. ATS-style keyword analysis
    # --------------------------------------------------

    ats_analysis = analyze_ats_keywords(
        resume_text,
        job_description
    )

    # --------------------------------------------------
    # 6. Resume statistics
    # --------------------------------------------------

    resume_statistics = analyze_resume_statistics(
        resume_text
    )

    # --------------------------------------------------
    # 7. Combine all results
    # --------------------------------------------------

    results = {
        "resume_text": resume_text,

        # Matching
        "match_score": match_score,

        # Skills
        "resume_skills": skill_analysis["resume_skills"],
        "job_skills": skill_analysis["job_skills"],
        "matching_skills": skill_analysis["matching_skills"],
        "missing_skills": skill_analysis["missing_skills"],
        "additional_skills": skill_analysis["additional_skills"],
        "skill_match_percentage": (
            skill_analysis["skill_match_percentage"]
        ),

        # ATS
        "ats_total_keywords": (
            ats_analysis["total_keywords"]
        ),
        "ats_matched_keywords": (
            ats_analysis["matched_keywords"]
        ),
        "ats_missing_keywords": (
            ats_analysis["missing_keywords"]
        ),
        "ats_keyword_coverage": (
            ats_analysis["keyword_coverage"]
        ),

        # Resume statistics
        "word_count": (
            resume_statistics["word_count"]
        ),
        "character_count": (
            resume_statistics["character_count"]
        ),
        "project_count": (
            resume_statistics["project_count"]
        ),
        "detected_sections": (
            resume_statistics["detected_sections"]
        ),
        "quality_checks": (
            resume_statistics["quality_checks"]
        ),

        # Recommendations
        "recommendations": recommendations
    }

    return results