import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import logging
import json
from io import StringIO

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_utils import setup_logging, JsonFormatter


class TestLoggingUtils(unittest.TestCase):
    """Test cases for the logging utilities"""
    
    def setUp(self):
        # Reset the root logger before each test
        self.root_logger = logging.getLogger()
        # Store original handlers to restore later
        self.original_handlers = self.root_logger.handlers.copy()
        self.original_level = self.root_logger.level
        # Clear handlers for this test
        self.root_logger.handlers = []
        self.root_logger.setLevel(logging.INFO)
        
    def tearDown(self):
        # Clean up by closing any handlers we created
        for handler in self.root_logger.handlers:
            handler.close()
        # Restore original handlers and level
        self.root_logger.handlers = self.original_handlers
        self.root_logger.setLevel(self.original_level)
    
    @patch('utils.logging_utils.LOG_FORMAT_TYPE', 'text')
    @patch('utils.logging_utils.LOG_FORMAT_STR', '%(levelname)s:%(message)s')
    def test_setup_logging_text_format(self):
        """Test setup_logging with text format"""
        # Create a string buffer to capture log output
        log_buffer = StringIO()
        
        # Mock logging handlers
        with patch('logging.FileHandler') as mock_file_handler, \
             patch('logging.StreamHandler') as mock_stream_handler:
            
            # Setup mock handlers
            mock_file_handler.return_value = MagicMock()
            mock_stream_handler.return_value = MagicMock()
            mock_stream_handler.return_value.stream = log_buffer
            
            # Call setup_logging
            setup_logging('test_log.txt')
            
            # Verify handlers were created
            mock_file_handler.assert_called_once_with('test_log.txt')
            mock_stream_handler.assert_called_once()
            
            # Verify formatter was set correctly
            formatter_calls = mock_file_handler.return_value.setFormatter.call_args[0]
            self.assertIsInstance(formatter_calls[0], logging.Formatter)
    
    @patch('utils.logging_utils.LOG_FORMAT_TYPE', 'json')
    def test_setup_logging_json_format(self):
        """Test setup_logging with JSON format"""
        # Mock logging handlers
        with patch('logging.FileHandler') as mock_file_handler, \
             patch('logging.StreamHandler') as mock_stream_handler:
            
            # Setup mock handlers
            mock_file_handler.return_value = MagicMock()
            mock_stream_handler.return_value = MagicMock()
            
            # Call setup_logging
            setup_logging('test_log.txt')
            
            # Verify formatter was set correctly
            formatter_calls = mock_file_handler.return_value.setFormatter.call_args[0]
            self.assertIsInstance(formatter_calls[0], JsonFormatter)
    
    def test_json_formatter(self):
        """Test JsonFormatter formats log records correctly"""
        # Create a formatter
        formatter = JsonFormatter()
        
        # Create a log record
        record = logging.LogRecord(
            name='test_logger',
            level=logging.ERROR,
            pathname='test_file.py',
            lineno=42,
            msg='Test error message',
            args=(),
            exc_info=None
        )
        
        # Format the record
        formatted = formatter.format(record)
        
        # Parse the JSON
        log_data = json.loads(formatted)
        
        # Verify fields
        self.assertEqual(log_data['level'], 'ERROR')
        self.assertEqual(log_data['message'], 'Test error message')
        self.assertEqual(log_data['logger'], 'test_logger')
        self.assertEqual(log_data['path'], 'test_file.py')
        self.assertEqual(log_data['line'], 42)


if __name__ == '__main__':
    unittest.main()
