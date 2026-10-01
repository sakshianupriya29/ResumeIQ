from resume_parser import extract_text_from_pdf
from job_ranker import rank_jobs


from pathlib import Path

PDF_PATH = Path(__file__).resolve().parent.parent / "sample_resumes" / "sample_resume.pdf"


jobs = [
    {
        "title": "Data Analyst",
        "description": """
        We are looking for a Data Analyst with experience in
        Python, SQL, Pandas, NumPy, Power BI, Tableau,
        statistics, data visualization and machine learning.
        """
    },

    {
        "title": "Machine Learning Engineer",
        "description": """
        We are looking for a Machine Learning Engineer with
        Python, TensorFlow, PyTorch, Scikit-learn, Deep Learning,
        NLP, Docker, AWS and machine learning experience.
        """
    },

    {
        "title": "Python Developer",
        "description": """
        We are looking for a Python Developer with strong
        Python programming skills, Flask, Django, APIs,
        Git, GitHub, SQL, databases and software development
        experience.
        """
    },

    {
        "title": "Frontend Developer",
        "description": """
        We are looking for a Frontend Developer with experience
        in HTML, CSS, JavaScript, React, TypeScript and
        frontend web development.
        """
    }
]


# Extract resume text
resume_text = extract_text_from_pdf(PDF_PATH)


# Rank jobs
ranked_jobs = rank_jobs(
    resume_text,
    jobs
)


print("=" * 70)
print("              RESUMEIQ - JOB MATCH RANKING")
print("=" * 70)

print("\nRanked Jobs")
print("-" * 70)

for rank, job in enumerate(ranked_jobs, start=1):

    print(
        f"{rank}. {job['title']:<25} "
        f"Match Score: {job['score']}%"
    )

print("\n" + "=" * 70)
print("              JOB RANKING COMPLETE!")
print("=" * 70)