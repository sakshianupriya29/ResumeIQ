from pipeline import analyze_resume_against_job


from pathlib import Path

PDF_PATH = Path(__file__).resolve().parent.parent / "sample_resumes" / "sample_resume.pdf"


JOB_DESCRIPTION = """
We are looking for a Data Analyst / Machine Learning candidate.

Required skills:
Python, SQL, Pandas, NumPy, Power BI, Tableau,
Machine Learning, Scikit-learn, AWS, Docker.

The candidate should have experience in data analysis,
data visualization, machine learning, statistics,
and building practical data-driven applications.
"""


results = analyze_resume_against_job(
    PDF_PATH,
    JOB_DESCRIPTION
)


print("=" * 70)
print("              RESUMEIQ - COMPLETE ANALYSIS")
print("=" * 70)


print("\nMATCH ANALYSIS")
print("-" * 70)

print(
    f"Overall Match Score: "
    f"{results['match_score']}%"
)

print(
    f"Skill Match Percentage: "
    f"{results['skill_match_percentage']}%"
)


print("\nATS ANALYSIS")
print("-" * 70)

print(
    f"Total Job Keywords: "
    f"{results['ats_total_keywords']}"
)

print(
    f"Matched Keywords: "
    f"{len(results['ats_matched_keywords'])}"
)

print(
    f"Missing Keywords: "
    f"{len(results['ats_missing_keywords'])}"
)

print(
    f"Keyword Coverage: "
    f"{results['ats_keyword_coverage']}%"
)


print("\nSKILL ANALYSIS")
print("-" * 70)

print(
    "Matching Skills: "
    + ", ".join(results["matching_skills"])
)

print(
    "Missing Skills: "
    + ", ".join(results["missing_skills"])
)

print(
    "Additional Skills: "
    + ", ".join(results["additional_skills"])
)


print("\nRESUME STATISTICS")
print("-" * 70)

print(
    f"Word Count: "
    f"{results['word_count']}"
)

print(
    f"Character Count: "
    f"{results['character_count']}"
)

print(
    f"Project Count: "
    f"{results['project_count']}"
)


print("\nRESUME SECTIONS")
print("-" * 70)

for section, detected in results[
    "detected_sections"
].items():

    status = "✓" if detected else "✗"

    print(
        f"{status} {section}"
    )


print("\nRECOMMENDATIONS")
print("-" * 70)

for i, recommendation in enumerate(
    results["recommendations"],
    start=1
):

    print(
        f"{i}. {recommendation}"
    )


print("\n" + "=" * 70)
print("              FULL ANALYSIS COMPLETE!")
print("=" * 70)