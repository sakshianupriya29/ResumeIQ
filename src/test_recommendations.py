from recommendations import generate_recommendations


missing_skills = [
    "AWS",
    "Docker",
    "Tableau"
]

matching_skills = [
    "Machine Learning",
    "NumPy",
    "Pandas",
    "Power BI",
    "Python",
    "SQL"
]

skill_match_percentage = 66.67


recommendations = generate_recommendations(
    missing_skills,
    matching_skills,
    skill_match_percentage
)


print("=" * 60)
print("           RESUMEIQ - RECOMMENDATIONS")
print("=" * 60)

for number, recommendation in enumerate(
    recommendations,
    start=1
):
    print(f"\n{number}. {recommendation}")

print("=" * 60)