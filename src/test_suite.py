import sys
import unittest
from pathlib import Path

# Allow the test suite to import modules directly from src/
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from preprocessing import clean_text
from matcher import calculate_match_score
from skills import extract_skills
from resume_parser import extract_text_from_pdf
from analyzer import analyze_skill_gap
from ats_analyzer import analyze_ats_keywords
from recommendations import generate_recommendations
from resume_stats import analyze_resume_statistics
from job_ranker import rank_jobs
from pipeline import analyze_resume_against_job


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "sample_resumes" / "sample_resume.pdf"


JOB_DESCRIPTION = """
We are looking for a Data Analyst / Machine Learning candidate.

Required skills:
Python, SQL, Pandas, NumPy, Machine Learning,
Scikit-learn, Power BI, AWS, Docker, Tableau.

The candidate should have experience in data analysis,
data visualization, statistics, and building practical
data-driven applications.
"""


class TestResumeIQ(unittest.TestCase):

    def test_clean_text(self):
        text = "Python, SQL & Pandas!"
        result = clean_text(text)

        self.assertIsInstance(result, str)
        self.assertIn("python", result)
        self.assertIn("sql", result)
        self.assertIn("pandas", result)

    def test_matcher(self):
        score = calculate_match_score(
            "Python SQL Pandas Machine Learning",
            "Python SQL Pandas Machine Learning"
        )

        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_skill_extraction(self):
        resume_text = """
        Python, SQL, Pandas, NumPy, Power BI and Machine Learning
        """

        skills = extract_skills(resume_text)

        self.assertIn("Python", skills)
        self.assertIn("SQL", skills)
        self.assertIn("Pandas", skills)
        self.assertIn("NumPy", skills)
        self.assertIn("Power BI", skills)

    def test_pdf_parser(self):
        self.assertTrue(
            PDF_PATH.exists(),
            f"Sample resume not found: {PDF_PATH}"
        )

        text = extract_text_from_pdf(PDF_PATH)

        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_skill_gap_analysis(self):
        resume_text = """
        Python SQL Pandas NumPy Power BI Machine Learning
        """

        result = analyze_skill_gap(
            resume_text,
            JOB_DESCRIPTION
        )

        self.assertIn("matching_skills", result)
        self.assertIn("missing_skills", result)
        self.assertIn("additional_skills", result)
        self.assertIn("skill_match_percentage", result)

        self.assertIsInstance(
            result["matching_skills"],
            list
        )

        self.assertIsInstance(
            result["missing_skills"],
            list
        )

    def test_ats_analysis(self):
        resume_text = """
        Python SQL Pandas NumPy Power BI Machine Learning
        """

        result = analyze_ats_keywords(
            resume_text,
            JOB_DESCRIPTION
        )

        self.assertIn("total_keywords", result)
        self.assertIn("matched_keywords", result)
        self.assertIn("missing_keywords", result)
        self.assertIn("keyword_coverage", result)

        self.assertGreaterEqual(
            result["keyword_coverage"],
            0
        )

        self.assertLessEqual(
            result["keyword_coverage"],
            100
        )

    def test_recommendations(self):
        recommendations = generate_recommendations(
            ["AWS", "Docker"],
            ["Python", "SQL"],
            50
        )

        self.assertIsInstance(
            recommendations,
            list
        )

        self.assertGreater(
            len(recommendations),
            0
        )

    def test_resume_statistics(self):
        resume_text = extract_text_from_pdf(PDF_PATH)

        result = analyze_resume_statistics(
            resume_text
        )

        self.assertIn("word_count", result)
        self.assertIn("character_count", result)
        self.assertIn("project_count", result)
        self.assertIn("detected_sections", result)
        self.assertIn("quality_checks", result)

        self.assertGreater(
            result["word_count"],
            0
        )

        self.assertGreater(
            result["character_count"],
            0
        )

    def test_job_ranking(self):
        resume_text = """
        Python SQL Pandas NumPy Machine Learning Power BI
        """

        jobs = [
            {
                "title": "Data Analyst",
                "description": """
                Python SQL Pandas NumPy Power BI
                """
            },
            {
                "title": "Frontend Developer",
                "description": """
                React JavaScript HTML CSS
                """
            },
            {
                "title": "Python Developer",
                "description": """
                Python SQL Django Flask
                """
            }
        ]

        results = rank_jobs(
            resume_text,
            jobs
        )

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)

        self.assertIn("title", results[0])
        self.assertIn("score", results[0])

        # Results should be sorted from highest to lowest score
        scores = [
            item["score"]
            for item in results
        ]

        self.assertEqual(
            scores,
            sorted(scores, reverse=True)
        )

    def test_complete_pipeline(self):
        self.assertTrue(
            PDF_PATH.exists(),
            f"Sample resume not found: {PDF_PATH}"
        )

        results = analyze_resume_against_job(
            PDF_PATH,
            JOB_DESCRIPTION
        )

        expected_keys = [
            "resume_text",
            "match_score",
            "resume_skills",
            "job_skills",
            "matching_skills",
            "missing_skills",
            "additional_skills",
            "skill_match_percentage",
            "ats_total_keywords",
            "ats_matched_keywords",
            "ats_missing_keywords",
            "ats_keyword_coverage",
            "word_count",
            "character_count",
            "project_count",
            "detected_sections",
            "quality_checks",
            "recommendations"
        ]

        for key in expected_keys:
            self.assertIn(
                key,
                results,
                f"Missing pipeline result: {key}"
            )

        self.assertIsInstance(
            results["resume_text"],
            str
        )

        self.assertGreater(
            len(results["resume_text"]),
            0
        )

        self.assertGreaterEqual(
            results["match_score"],
            0
        )

        self.assertLessEqual(
            results["match_score"],
            100
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)