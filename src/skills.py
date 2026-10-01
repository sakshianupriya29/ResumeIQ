import pandas as pd
import re
from pathlib import Path


# Find the ResumeIQ project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to the skill database
SKILLS_FILE = PROJECT_ROOT / "data" / "skills" / "skills.csv"


def load_skills():
    """
    Load the skill database from CSV.
    """
    return pd.read_csv(SKILLS_FILE)


def extract_skills(text):
    """
    Identify skills present in a piece of text.
    """

    skills_df = load_skills()

    text_lower = text.lower()

    found_skills = []

    for skill in skills_df["skill"]:

        # Escape special characters so skills like C++ and Node.js work correctly
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))