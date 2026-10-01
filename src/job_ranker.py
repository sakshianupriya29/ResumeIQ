from matcher import calculate_match_score


def rank_jobs(resume_text, jobs):
    """
    Calculate resume-job match scores and rank jobs.

    Parameters:
        resume_text: Resume text
        jobs: List of dictionaries containing job title and description

    Returns:
        List of jobs sorted by match score from highest to lowest.
    """

    results = []

    for job in jobs:

        score = calculate_match_score(
            resume_text,
            job["description"]
        )

        results.append({
            "title": job["title"],
            "score": score
        })

    # Sort jobs by score
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results