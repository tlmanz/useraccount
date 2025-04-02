import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import requests

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api import create_user


class TestAPI(unittest.TestCase):
    """Test cases for the API module"""
    
    @patch('utils.api.requests.post')
    def test_successful_user_creation(self, mock_post):
        """Test successful user creation"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"success": True, "message": "User created successfully"}
        mock_post.return_value = mock_response
        
        # Test data
        user_data = {"email": "test@example.com", "name": "Test User", "role": "user"}
        
        # Call function
        success, message = create_user(user_data)
        
        # Assertions
        self.assertTrue(success)
        self.assertEqual(message, "")
        mock_post.assert_called_once()
    
    @patch('utils.api.requests.post')
    def test_api_error_response(self, mock_post):
        """Test API error response handling"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"success": False, "message": "Email already exists"}
        mock_post.return_value = mock_response
        
        # Test data
        user_data = {"email": "existing@example.com", "name": "Existing User", "role": "user"}
        
        # Call function
        success, message = create_user(user_data)
        
        # Assertions
        self.assertFalse(success)
        self.assertIn("Email already exists", message)
    
    @patch('utils.api.requests.post')
    def test_connection_error_with_retry(self, mock_post):
        """Test connection error with retry logic"""
        # Setup mock to raise ConnectionError on first call, then succeed
        mock_post.side_effect = [
            requests.exceptions.ConnectionError("Connection refused"),
            MagicMock(status_code=201, json=lambda: {"success": True, "message": "User created successfully"})
        ]
        
        # Test data
        user_data = {"email": "test@example.com", "name": "Test User", "role": "user"}
        
        # Call function with max_retries=1 to make test faster
        success, message = create_user(user_data, max_retries=1)
        
        # Assertions
        self.assertTrue(success)
        self.assertEqual(message, "")
        self.assertEqual(mock_post.call_count, 2)  # Should be called twice due to retry
    
    @patch('utils.api.requests.post')
    def test_max_retries_exceeded(self, mock_post):
        """Test max retries exceeded"""
        # Setup mock to always raise ConnectionError
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Test data
        user_data = {"email": "test@example.com", "name": "Test User", "role": "user"}
        
        # Call function with max_retries=2 to make test faster
        success, message = create_user(user_data, max_retries=2)
        
        # Assertions
        self.assertFalse(success)
        self.assertIn("Request failed after 2 retries", message)
        self.assertEqual(mock_post.call_count, 3)  # Initial attempt + 2 retries


if __name__ == "__main__":
    unittest.main()
