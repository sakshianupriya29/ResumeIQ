from matcher import calculate_match_score


resume = """
Graphic designer with experience in Adobe Photoshop,
Illustrator, UI design, branding, typography and visual
communication. Worked on marketing campaigns and creative
design projects for various clients.
"""

job_description = """
We are looking for a Python developer with experience
in machine learning, data analysis, SQL, pandas,
NumPy and scikit-learn.
"""

score = calculate_match_score(
    resume,
    job_description
)

print("=" * 50)
print("        RESUMEIQ - NLP MATCHING TEST")
print("=" * 50)
print(f"Resume-Job Match Score: {score}%")
print("=" * 50)