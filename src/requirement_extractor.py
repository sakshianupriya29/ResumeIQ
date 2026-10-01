import re
from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SKILLS_FILE = (
    PROJECT_ROOT
    / "data"
    / "skills"
    / "skills.csv"
)


# ============================================================
# GENERIC STOP WORDS
# ============================================================

STOP_WORDS = {
    "about", "above", "across", "after", "again", "against",
    "also", "any", "around", "as", "at", "be", "because",
    "been", "before", "being", "below", "between", "both",
    "but", "by", "can", "could", "did", "do", "does", "doing",
    "down", "during", "each", "for", "from", "further", "get",
    "gets", "getting", "give", "given", "good", "has", "have",
    "having", "how", "if", "in", "into", "is", "it", "its",
    "just", "may", "more", "most", "must", "of", "on", "only",
    "or", "other", "our", "out", "over", "per", "please",
    "required", "requirements", "role", "same", "should", "so",
    "some", "such", "than", "that", "the", "their", "them",
    "then", "there", "these", "they", "this", "those", "through",
    "to", "under", "up", "upon", "us", "use", "used", "using",
    "very", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "will", "with", "within", "would",
    "you", "your"
}


# ============================================================
# LEADING WORDS
# ============================================================

LEADING_WORDS = {
    "in",
    "of",
    "with",
    "using",
    "knowledge",
    "experience",
    "expertise",
    "proficiency",
    "proficient",
    "familiarity",
    "skills",
    "skill",
    "strong",
    "hands-on",
    "hands",
    "working",
    "expert",
    "expertise"
}


# ============================================================
# REQUIREMENT CUES
# ============================================================

REQUIREMENT_CUES = [
    "experience with",
    "experience in",
    "proficiency in",
    "proficient in",
    "knowledge of",
    "knowledge in",
    "expertise in",
    "skilled in",
    "skills in",
    "strong skills in",
    "hands-on experience with",
    "hands on experience with",
    "familiarity with",
    "working knowledge of",
    "tools such as",
    "technologies such as"
]


# ============================================================
# RESPONSIBILITY CUES
# ============================================================

RESPONSIBILITY_CUES = [
    "ability to",
    "responsible for",
    "responsibilities include",
    "will be responsible",
    "you will",
    "should be able",
    "expected to",
    "duties include",
    "role involves",
    "work on",
    "work with",
    "develop and",
    "create and",
    "manage and",
    "prepare and",
    "analyze and",
    "maintain and"
]


# ============================================================
# COMMON TRAILING DESCRIPTORS
# ============================================================

TRAILING_DESCRIPTORS = {
    "cloud",
    "services",
    "service",
    "systems",
    "system",
    "tools",
    "tool",
    "platform",
    "platforms",
    "technology",
    "technologies",
    "applications",
    "application",
    "software",
    "solutions",
    "solution",
    "databases",
    "database",
    "environment",
    "environments"
    "cloud",
    "cloud services",
    "cloud technology",
    "cloud technologies",
}


# ============================================================
# LOAD KNOWN SKILLS
# ============================================================

def load_known_skills():
    """
    Load structured skills from skills.csv.
    """

    if not SKILLS_FILE.exists():
        return []

    skills_df = pd.read_csv(SKILLS_FILE)

    return [
        str(skill).strip()
        for skill in skills_df["skill"]
        if str(skill).strip()
    ]


# ============================================================
# NORMALIZE TERM
# ============================================================

def normalize_term(term):
    """
    Normalize a requirement for comparison.
    """

    term = str(term).lower().strip()

    # Remove bullets/numbers.
    term = re.sub(
        r"^[\-\•\*\d\.\)\(]+\s*",
        "",
        term
    )

    # Normalize punctuation.
    term = re.sub(
        r"[/|]+",
        " ",
        term
    )

    term = re.sub(
        r"\s+",
        " ",
        term
    )

    term = term.strip(
        " ,;:.-"
    )

    # Remove introductory words repeatedly.
    changed = True

    while changed:

        changed = False

        words = term.split()

        if words and words[0] in LEADING_WORDS:

            words = words[1:]

            term = " ".join(words)

            changed = True

    return term.strip()


# ============================================================
# REMOVE TRAILING DESCRIPTORS
# ============================================================

def remove_trailing_descriptor(term):
    """
    Remove generic descriptive words from the end of a
    requirement.

    Examples:
        AWS cloud services -> AWS
        SQL databases -> SQL
        AWS cloud technology -> AWS
    """

    words = term.split()

    while len(words) > 1:

        if words[-1] in TRAILING_DESCRIPTORS:
            words.pop()
        else:
            break

    return " ".join(words)


# ============================================================
# CLEAN PHRASE
# ============================================================

def clean_phrase(phrase):
    """
    Clean grammatical fragments from a candidate.
    """

    phrase = normalize_term(
        phrase
    )

    # Remove introductory prepositions.
    phrase = re.sub(
        r"^(in|of|with|for|to|on|at|by)\s+",
        "",
        phrase,
        flags=re.IGNORECASE
    )

    # Remove trailing conjunctions.
    phrase = re.sub(
        r"\s+(and|or|as|such as)$",
        "",
        phrase,
        flags=re.IGNORECASE
    )

    phrase = phrase.strip(
        " ,;:.-"
    )

    return phrase


# ============================================================
# RESPONSIBILITY CHECK
# ============================================================

def is_responsibility_phrase(candidate):
    """
    Identify phrases that describe job duties rather than
    skills or professional requirements.
    """

    candidate_lower = candidate.lower().strip()

    for cue in RESPONSIBILITY_CUES:

        if candidate_lower.startswith(cue):
            return True

    responsibility_patterns = [
        r"^ability to ",
        r"^responsible for ",
        r"^expected to ",
        r"^you will ",
        r"^will be ",
        r"^duties include ",
        r"^role involves ",
        r"^maintain ",
        r"^develop ",
        r"^create ",
        r"^prepare ",
        r"^analyze ",
        r"^manage ",
        r"^coordinate ",
        r"^support ",
        r"^assist "
    ]

    for pattern in responsibility_patterns:

        if re.search(
            pattern,
            candidate_lower
        ):
            return True

    return False


# ============================================================
# VALIDATE CANDIDATE
# ============================================================

def is_valid_candidate(candidate):
    """
    Check whether a phrase is likely to be a meaningful
    professional requirement.
    """

    candidate = clean_phrase(
        candidate
    )

    if not candidate:
        return False

    if is_responsibility_phrase(
        candidate
    ):
        return False

    words = candidate.split()

    # Avoid extremely long sentence fragments.
    if len(words) > 5:
        return False

    if len(candidate) < 2:
        return False

    meaningful_words = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    if not meaningful_words:
        return False

    bad_phrases = {
        "looking for",
        "we are",
        "years",
        "years experience",
        "ability",
        "responsible",
        "responsible for",
        "work",
        "work with",
        "work on",
        "good communication",
        "strong communication",
        "team player",
        "problem solving",
        "job description",
        "job requirements",
        "professional",
        "candidate",
        "candidates"
    }

    if candidate in bad_phrases:
        return False

    return True


# ============================================================
# EXTRACT KNOWN SKILLS
# ============================================================

def extract_known_skills(text):
    """
    Detect skills explicitly present in skills.csv.
    """

    if not text:
        return []

    text_lower = text.lower()

    known_skills = load_known_skills()

    found = []

    for skill in known_skills:

        pattern = (
            r"(?<!\w)"
            + re.escape(
                skill.lower()
            )
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text_lower
        ):

            found.append(
                skill
            )

    return sorted(
        set(found),
        key=str.lower
    )


# ============================================================
# SPLIT REQUIREMENT LIST
# ============================================================

def split_requirement_list(text):
    """
    Split lists such as:

    Talent Acquisition, Employee Relations, Payroll and Workday

    into:

    Talent Acquisition
    Employee Relations
    Payroll
    Workday
    """

    if not text:
        return []

    parts = re.split(
        r",|\||/",
        text
    )

    final_parts = []

    for part in parts:

        sub_parts = re.split(
            r"\s+(?:and|or)\s+",
            part,
            flags=re.IGNORECASE
        )

        for sub_part in sub_parts:

            cleaned = clean_phrase(
                sub_part
            )

            if is_valid_candidate(
                cleaned
            ):

                final_parts.append(
                    cleaned
                )

    return final_parts


# ============================================================
# EXTRACT CUE-BASED REQUIREMENTS
# ============================================================

def extract_cue_candidates(text):
    """
    Extract requirements from phrases such as:

    experience with X
    experience in X
    knowledge of X
    proficiency in X
    familiarity with X
    """

    if not text:
        return []

    candidates = []

    # Convert newlines to spaces.
    normalized_text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # Split sentences.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        normalized_text
    )

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_lower = sentence.lower()

        for cue in REQUIREMENT_CUES:

            match = re.search(
                re.escape(cue),
                sentence_lower
            )

            if not match:
                continue

            remaining = sentence[
                match.end():
            ]

            remaining = re.split(
                r"[.;:!?]",
                remaining
            )[0]

            candidates.extend(
                split_requirement_list(
                    remaining
                )
            )

    return candidates


# ============================================================
# EXTRACT BULLET REQUIREMENTS
# ============================================================

def extract_bullet_candidates(text):
    """
    Extract likely requirements from bullet points.
    """

    if not text:
        return []

    candidates = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove bullet markers.
        line = re.sub(
            r"^[\-\•\*\d\.\)\(]+\s*",
            "",
            line
        )

        signal = re.search(
            r"\b("
            r"experience|proficiency|knowledge|expertise|"
            r"skills?|familiarity|certification|certified|"
            r"expert|proficient|required|"
            r"must|strong|hands[- ]on"
            r")\b",
            line,
            flags=re.IGNORECASE
        )

        if not signal:
            continue

        # Remove introductory requirement wording.
        line = re.sub(
            r"^(experience|knowledge|proficiency|"
            r"expertise|skills?|familiarity|"
            r"strong|hands[- ]on)"
            r"\s*(in|with|of)?\s*",
            "",
            line,
            flags=re.IGNORECASE
        )

        candidates.extend(
            split_requirement_list(
                line
            )
        )

    return candidates


# ============================================================
# EXTRACT DYNAMIC REQUIREMENTS
# ============================================================

def extract_dynamic_requirements(text):
    """
    Detect professional requirements that may not exist
    in skills.csv.
    """

    if not text:
        return []

    candidates = []

    candidates.extend(
        extract_cue_candidates(
            text
        )
    )

    candidates.extend(
        extract_bullet_candidates(
            text
        )
    )

    cleaned_candidates = []

    for candidate in candidates:

        candidate = clean_phrase(
            candidate
        )

        if is_valid_candidate(
            candidate
        ):

            cleaned_candidates.append(
                candidate
            )

    return sorted(
        set(cleaned_candidates),
        key=str.lower
    )


# ============================================================
# REMOVE DUPLICATE VARIANTS
# ============================================================

def remove_duplicate_variants(
    requirements,
    known_skills
):
    """
    Remove dynamic variants when a structured skill
    already represents the same requirement.

    Examples:

    AWS + AWS cloud services
        -> AWS

    SQL + SQL databases
        -> SQL
    """

    known_normalized = {
        normalize_term(skill): skill
        for skill in known_skills
    }

    final = []

    for requirement in requirements:

        normalized = normalize_term(
            requirement
        )

        # Direct duplicate.
        if normalized in known_normalized:
            continue

        shortened = remove_trailing_descriptor(
            normalized
        )

        # If shortened form matches a known skill,
        # discard the longer variant.
        if shortened in known_normalized:
            continue

        final.append(
            requirement
        )

    return sorted(
        set(final),
        key=str.lower
    )


# ============================================================
# COMBINED JOB REQUIREMENTS
# ============================================================

def extract_job_requirements(text):
    """
    Return structured skills plus dynamically detected
    professional requirements.
    """

    known_skills = extract_known_skills(
        text
    )

    dynamic_requirements = (
        extract_dynamic_requirements(
            text
        )
    )

    dynamic_requirements = (
        remove_duplicate_variants(
            dynamic_requirements,
            known_skills
        )
    )

    all_requirements = sorted(
        set(
            known_skills
            +
            dynamic_requirements
        ),
        key=str.lower
    )

    return {
        "known_skills": sorted(
            set(known_skills),
            key=str.lower
        ),

        "dynamic_requirements": dynamic_requirements,

        "all_requirements": all_requirements
    }


# ============================================================
# RESUME TERMS
# ============================================================

def extract_resume_terms(text):
    """
    Extract terms from a resume.

    Known skills are always included.
    Dynamic terms are included when they can be
    identified as professional requirements.
    """

    if not text:
        return []

    known_skills = extract_known_skills(
        text
    )

    dynamic_terms = extract_dynamic_requirements(
        text
    )

    dynamic_terms = (
        remove_duplicate_variants(
            dynamic_terms,
            known_skills
        )
    )

    return sorted(
        set(
            known_skills
            +
            dynamic_terms
        ),
        key=str.lower
    )