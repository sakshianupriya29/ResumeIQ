from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import clean_text


def calculate_match_score(resume_text, job_description):
    """
    Calculate similarity between a resume and a job description
    using TF-IDF and cosine similarity.
    """

    # Clean both documents
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_description)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    # Convert documents into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(
        [resume_clean, job_clean]
    )

    # Calculate cosine similarity
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    # Convert similarity into percentage
    match_score = similarity * 100

    return round(match_score, 2)