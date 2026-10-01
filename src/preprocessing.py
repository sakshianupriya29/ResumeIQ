import re


def clean_text(text):
    """
    Clean and normalize resume/job description text.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Keep letters, numbers, and basic symbols
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text