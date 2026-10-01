from analyzer import analyze_skill_gap


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


result = analyze_skill_gap(
    resume,
    job_description
)


print("=" * 60)
print("             RESUMEIQ - SKILL GAP ANALYSIS")
print("=" * 60)

print(
    f"\nSkill Match Score: "
    f"{result['skill_match_percentage']}%"
)

print("\nMATCHING SKILLS:")
for skill in result["matching_skills"]:
    print(f"  ✓ {skill}")

print("\nMISSING SKILLS:")
for skill in result["missing_skills"]:
    print(f"  ✗ {skill}")

print("\nADDITIONAL RESUME SKILLS:")
for skill in result["additional_skills"]:
    print(f"  + {skill}")

print("=" * 60)