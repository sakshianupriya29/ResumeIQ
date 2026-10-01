from resume_parser import extract_text_from_pdf


from pathlib import Path

PDF_PATH = Path(__file__).resolve().parent.parent / "sample_resumes" / "sample_resume.pdf"


try:
    text = extract_text_from_pdf(PDF_PATH)

    print("=" * 60)
    print("          RESUMEIQ - PDF PARSER TEST")
    print("=" * 60)

    print(f"\nExtracted characters: {len(text)}")

    print("\nEXTRACTED RESUME TEXT:")
    print("-" * 60)

    print(text[:3000])

    print("\n" + "=" * 60)
    print("PDF extraction successful!")
    print("=" * 60)

except Exception as e:

    print("=" * 60)
    print("PDF PARSER ERROR")
    print("=" * 60)

    print(f"\n{e}")