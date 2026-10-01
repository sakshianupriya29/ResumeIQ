from resume_parser import extract_text_from_pdf
from resume_stats import analyze_resume_statistics


from pathlib import Path

PDF_PATH = Path(__file__).resolve().parent.parent / "sample_resumes" / "sample_resume.pdf"

# Extract resume text
resume_text = extract_text_from_pdf(PDF_PATH)


# Analyze resume
results = analyze_resume_statistics(
    resume_text
)


print("=" * 70)
print("              RESUMEIQ - RESUME STATISTICS")
print("=" * 70)

print("\nBASIC STATISTICS")
print("-" * 70)

print(
    f"Word Count:       "
    f"{results['word_count']}"
)

print(
    f"Character Count:  "
    f"{results['character_count']}"
)

print(
    f"Project Count:    "
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


print("\nQUALITY CHECKS")
print("-" * 70)

for i, check in enumerate(
    results["quality_checks"],
    start=1
):

    print(
        f"{i}. {check}"
    )


print("\n" + "=" * 70)
print("              RESUME STATISTICS COMPLETE!")
print("=" * 70)