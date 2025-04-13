import unittest
from unittest.mock import MagicMock, patch
import datetime
import gspread
from services.google_sheets import GoogleSheetsService
from models.news import ProcessedSubmission

class TestGoogleSheetsService(unittest.TestCase):
    
    @patch('services.google_sheets.service_account')
    @patch('services.google_sheets.gspread')
    def setUp(self, mock_gspread, mock_service_account):
        # Setup mock objects
        self.mock_client = MagicMock()
        self.mock_sheet = MagicMock()
        self.mock_worksheet = MagicMock()
        
        # Configure mocks
        mock_gspread.authorize.return_value = self.mock_client
        self.mock_client.open_by_key.return_value = self.mock_sheet
        self.mock_sheet.worksheet.return_value = self.mock_worksheet
        
        # Initialize service without calling _initialize_sheets
        with patch.object(GoogleSheetsService, '_initialize_sheets') as patched_init:
            self.service = GoogleSheetsService()
            patched_init.assert_called_once()
        
        # Replace actual sheet with mock
        self.service.submissions_sheet = self.mock_worksheet
    
    def test_initialize_sheets_existing(self):
        # Test case when sheet already exists
        self.mock_sheet.worksheet.return_value = self.mock_worksheet
        self.service._initialize_sheets()
        self.mock_sheet.worksheet.assert_called_with("Submissions")
        self.mock_sheet.add_worksheet.assert_not_called()
    
    def test_initialize_sheets_create_new(self):
        # Test case when sheet doesn't exist
        self.mock_sheet.worksheet.side_effect = gspread.exceptions.WorksheetNotFound
        self.mock_sheet.add_worksheet.return_value = self.mock_worksheet
        
        self.service._initialize_sheets()
        
        self.mock_sheet.add_worksheet.assert_called_once_with(
            title="Submissions", rows=1000, cols=10
        )
        self.mock_worksheet.append_row.assert_called_once()
    
    def test_get_all_submissions(self):
        # Mock data to be returned with sufficiently long description
        long_description = "This is a test description that is at least fifty characters long to pass validation requirements for the ProcessedSubmission model."
        mock_records = [
            {"ID": "123", "Timestamp": "2023-01-01T12:00:00", "Title": "Test News", 
             "Description": long_description, "City": "Test City", "Category": "Test Category",
             "Publisher Name": "Test Publisher", "Publisher Phone": "1234567890",
             "Image Path": "/path/to/image.jpg", "Status": "approved"}
        ]
        self.mock_worksheet.get_all_records.return_value = mock_records
        
        # Call method
        submissions = self.service.get_all_submissions()
        
        # Verify results
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0].id, "123")
        self.assertEqual(submissions[0].news_title, "Test News")
        self.assertEqual(submissions[0].status, "approved")
    
    def test_add_submission(self):
        # Create test submission with sufficiently long description
        long_description = "This is a test description that is at least fifty characters long to pass validation requirements for the ProcessedSubmission model."
        test_submission = ProcessedSubmission(
            id="test123",
            timestamp=datetime.datetime.fromisoformat("2023-01-01T12:00:00"),
            news_title="Test Title",
            news_description=long_description,
            city="Test City",
            category="Test Category",
            publisher_name="Test Publisher",
            publisher_phone="1234567890",
            image_path="/path/to/image.jpg",
            status="pending"
        )
        
        # Call method
        self.service.add_submission(test_submission)
        
        # Verify worksheet method was called with correct data
        self.mock_worksheet.append_row.assert_called_once()
        args = self.mock_worksheet.append_row.call_args[0][0]
        self.assertEqual(args[0], "test123")
        self.assertEqual(args[2], "Test Title")
        self.assertEqual(args[9], "pending")
    
    def test_update_submission_status(self):
        # Mock data
        mock_records = [
            {"ID": "123", "Description": "Test Description", "Status": "pending"}
        ]
        self.mock_worksheet.get_all_records.return_value = mock_records
        
        # Call method
        result = self.service.update_submission_status("123", "approved")
        
        # Verify results
        self.assertTrue(result)
        self.mock_worksheet.update_cell.assert_called_once_with(2, 10, "approved")
    
    def test_update_submission_status_with_duplicate(self):
        # Mock data
        mock_records = [
            {"ID": "123", "Description": "Test Description", "Status": "pending"}
        ]
        self.mock_worksheet.get_all_records.return_value = mock_records
        
        # Call method
        result = self.service.update_submission_status("123", "duplicate", duplicate_of="456")
        
        # Verify results
        self.assertTrue(result)
        self.assertEqual(self.mock_worksheet.update_cell.call_count, 2)
        # First call updates status
        self.mock_worksheet.update_cell.assert_any_call(2, 10, "duplicate")
        # Second call updates description
        self.mock_worksheet.update_cell.assert_any_call(
            2, 4, "Test Description [DUPLICATE of 456]"
        )
    
    def test_update_submission_status_not_found(self):
        # Mock data with different ID
        mock_records = [
            {"ID": "456", "Description": "Other Description", "Status": "pending"}
        ]
        self.mock_worksheet.get_all_records.return_value = mock_records
        
        # Call method with non-existent ID
        result = self.service.update_submission_status("123", "approved")
        
        # Verify results
        self.assertFalse(result)
        self.mock_worksheet.update_cell.assert_not_called()

if __name__ == '__main__':
    unittest.main()
