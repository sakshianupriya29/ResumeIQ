def generate_recommendations(
    missing_skills,
    matching_skills,
    skill_match_percentage
):
    """
    Generate resume improvement recommendations
    based on skill gaps and matching skills.
    """

    recommendations = []

    # Overall skill coverage
    if skill_match_percentage < 50:
        recommendations.append(
            "Your resume covers less than half of the "
            "skills mentioned in the job description. "
            "Review the job requirements and highlight "
            "relevant experience where applicable."
        )

    elif skill_match_percentage < 75:
        recommendations.append(
            "Your resume has moderate skill coverage. "
            "Consider strengthening the skills that are "
            "currently missing from your resume."
        )

    else:
        recommendations.append(
            "Your resume has strong coverage of the "
            "skills identified in this job description."
        )

    # Missing skill recommendations
    for skill in missing_skills:

        recommendations.append(
            f"Consider highlighting relevant experience, "
            f"projects, coursework, or certifications "
            f"related to {skill} if applicable."
        )

    # Matching skills
    if matching_skills:
        recommendations.append(
            "Make sure your strongest matching skills are "
            "clearly visible in your Skills and Projects "
            "sections."
        )

    return recommendations