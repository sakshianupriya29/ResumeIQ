from skills import extract_skills


resume = """
B.Tech student with experience in Python, SQL, Pandas,
NumPy, Machine Learning and Scikit-learn.

Developed machine learning projects using Python and
worked with data analysis and visualization using
Matplotlib and Power BI.
"""


job_description = """
We are looking for a Data Analyst with strong Python,
SQL, Pandas and NumPy skills.

The candidate should have experience with Power BI,
Tableau, Machine Learning, AWS and Docker.
"""


resume_skills = extract_skills(resume)
job_skills = extract_skills(job_description)

matching_skills = sorted(
    set(resume_skills) & set(job_skills)
)

missing_skills = sorted(
    set(job_skills) - set(resume_skills)
)


print("=" * 60)
print("              RESUMEIQ - SKILL ANALYSIS")
print("=" * 60)

print("\nRESUME SKILLS:")
for skill in resume_skills:
    print(f"  ✓ {skill}")

print("\nJOB REQUIRED SKILLS:")
for skill in job_skills:
    print(f"  • {skill}")

print("\nMATCHING SKILLS:")
for skill in matching_skills:
    print(f"  ✓ {skill}")

print("\nMISSING SKILLS:")
for skill in missing_skills:
    print(f"  ✗ {skill}")

print("=" * 60)