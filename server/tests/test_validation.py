import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.validation import validate_submission
from models import NewsSubmission

class TestValidationService(unittest.TestCase):
    def test_valid_submission(self):
        """Test a valid submission"""
        submission = NewsSubmission(
            title="Test News Title",
            description="This is a test description that is longer than fifty characters to meet the minimum length requirement.",
            city="Test City",
            category="Test Category",
            publisher_name="Test Publisher",
            publisher_phone="1234567890",
            image_path="test_image.jpg"
        )
        
        result = validate_submission(submission)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
    
    def test_missing_fields(self):
        """Test submission with missing fields"""
        submission = NewsSubmission(
            title="",
            description="Short desc",
            city="Test City",
            category="Test Category",
            publisher_name="Test Publisher",
            publisher_phone="1234567890",
            image_path="test_image.jpg"
        )
        
        result = validate_submission(submission)
        self.assertFalse(result.is_valid)
        self.assertGreaterEqual(len(result.errors), 1)
        self.assertTrue(any("title" in error.lower() for error in result.errors))
    
    def test_short_description(self):
        """Test submission with description that is too short"""
        submission = NewsSubmission(
            title="Test News Title",
            description="Too short",
            city="Test City",
            category="Test Category",
            publisher_name="Test Publisher",
            publisher_phone="1234567890",
            image_path="test_image.jpg"
        )
        
        result = validate_submission(submission)
        self.assertFalse(result.is_valid)
        self.assertGreaterEqual(len(result.errors), 1)
        self.assertTrue(any("description" in error.lower() for error in result.errors))
        
    def test_missing_image(self):
        """Test submission without an image"""
        submission = NewsSubmission(
            title="Test News Title",
            description="This is a test description that is longer than fifty characters to meet the minimum length requirement.",
            city="Test City",
            category="Test Category",
            publisher_name="Test Publisher",
            publisher_phone="1234567890",
            image_path=None
        )
        
        result = validate_submission(submission)
        self.assertFalse(result.is_valid)
        self.assertGreaterEqual(len(result.errors), 1)
        self.assertTrue(any("image" in error.lower() for error in result.errors))

if __name__ == "__main__":
    unittest.main()
