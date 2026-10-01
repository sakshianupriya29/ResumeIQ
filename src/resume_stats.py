import re


def analyze_resume_statistics(resume_text):
    """
    Analyze basic statistics and structural information
    from a resume.
    """

    # Basic text statistics
    words = re.findall(r"\b[\w+#.-]+\b", resume_text)

    word_count = len(words)
    character_count = len(resume_text)

    # Detect common resume sections
    section_names = {
        "Summary": ["summary", "objective", "profile"],
        "Technical Skills": ["technical skills", "skills"],
        "Projects": ["projects", "project"],
        "Experience": [
            "experience",
            "work experience",
            "internship"
        ],
        "Education": ["education"],
        "Certifications": [
            "certifications",
            "certificates"
        ]
    }

    detected_sections = {}

    resume_lower = resume_text.lower()

    for section, keywords in section_names.items():

        found = any(
            keyword in resume_lower
            for keyword in keywords
        )

        detected_sections[section] = found

    # Count projects only inside the Projects section
    project_count = 0

    projects_match = re.search(
        r"PROJECTS(.*?)(?=\nEXPERIENCE|\nEDUCATION|\nCERTIFICATIONS|$)",
        resume_text,
        re.IGNORECASE | re.DOTALL
    )

    if projects_match:
        projects_section = projects_match.group(1)

        # Project headings in the resume contain "|"
        project_lines = []

        for line in projects_section.splitlines():
            line = line.strip()

            if "|" in line and len(line) > 10:
                project_lines.append(line)

        project_count = len(project_lines)

    # Simple quality checks
    quality_checks = []

    if word_count < 250:
        quality_checks.append(
            "Resume appears relatively short."
        )
    elif word_count > 900:
        quality_checks.append(
            "Resume may be longer than necessary."
        )
    else:
        quality_checks.append(
            "Resume length is within a reasonable range."
        )

    if detected_sections["Technical Skills"]:
        quality_checks.append(
            "Technical Skills section detected."
        )
    else:
        quality_checks.append(
            "Technical Skills section not detected."
        )

    if detected_sections["Projects"]:
        quality_checks.append(
            "Projects section detected."
        )
    else:
        quality_checks.append(
            "Projects section not detected."
        )

    if detected_sections["Experience"]:
        quality_checks.append(
            "Experience section detected."
        )
    else:
        quality_checks.append(
            "Experience section not detected."
        )

    if detected_sections["Education"]:
        quality_checks.append(
            "Education section detected."
        )
    else:
        quality_checks.append(
            "Education section not detected."
        )

    if detected_sections["Certifications"]:
        quality_checks.append(
            "Certifications section detected."
        )
    else:
        quality_checks.append(
            "Certifications section not detected."
        )

    return {
        "word_count": word_count,
        "character_count": character_count,
        "project_count": project_count,
        "detected_sections": detected_sections,
        "quality_checks": quality_checks
    }