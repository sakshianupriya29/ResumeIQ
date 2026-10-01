from resume_parser import extract_text_from_pdf
from ats_analyzer import analyze_ats_keywords


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


# Extract resume text
resume_text = extract_text_from_pdf(PDF_PATH)


# Analyze ATS-style keywords
results = analyze_ats_keywords(
    resume_text,
    JOB_DESCRIPTION
)


print("=" * 70)
print("             RESUMEIQ - ATS KEYWORD ANALYSIS")
print("=" * 70)

print("\nTOTAL JOB KEYWORDS")
print("-" * 70)
print(results["total_keywords"])

print("\nMATCHED KEYWORDS")
print("-" * 70)

for keyword in results["matched_keywords"]:
    print(f"✓ {keyword}")

print("\nMISSING KEYWORDS")
print("-" * 70)

for keyword in results["missing_keywords"]:
    print(f"✗ {keyword}")

print("\nKEYWORD COVERAGE")
print("-" * 70)
print(f"{results['keyword_coverage']}%")

print("\n" + "=" * 70)
print("             ATS ANALYSIS COMPLETE!")
print("=" * 70)