import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.resume_generator import generate_resume_pdf
from src.portfolio_generator import generate_portfolio_html


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.profile = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "location": "Test City",
            "linkedin": "",
            "website": "",
            "summary": "Python developer",
            "skills": ["Python", "SQL"],
            "experience": [],
            "education": [],
            "projects": [],
        }

    def test_resume_returns_pdf_bytes(self):
        result = generate_resume_pdf(self.profile)
        self.assertIsInstance(result, bytes)
        self.assertTrue(result.startswith(b"%PDF"))

    def test_portfolio_contains_profile_name(self):
        result = generate_portfolio_html(self.profile)
        self.assertIn("Test User", result)
        self.assertIn("<html", result.lower())


if __name__ == "__main__":
    unittest.main()
