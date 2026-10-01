from resume_parser import extract_text_from_pdf
from pipeline import analyze_resume_against_job
from report_generator import generate_analysis_report


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


# Run complete ResumeIQ analysis
results = analyze_resume_against_job(
    PDF_PATH,
    JOB_DESCRIPTION
)


# Generate report
report = generate_analysis_report(
    results
)


print(report)

print("\n")
print("=" * 70)
print("REPORT GENERATION SUCCESSFUL!")
print("=" * 70)