import logging
import os
import unittest

from client import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.test_log_file = "Dan_test/Connect_to_server/test.log"
        if os.path.exists(self.test_log_file):
          os.remove(self.test_log_file)
        
    def _tearDown(self):
        # Clean up test log file
        if os.path.exists(self.test_log_file):
          os.remove(self.test_log_file)
        
    def test_info_log_level(self):
        # Create logger with INFO level
        logger = Logger("TestLogger", log_level=logging.INFO, log_path=self.test_log_file)
        test_message = "Test message"
        
        # Log messages at different levels
        logger.debug(test_message)
        logger.info(test_message)
        logger.success(test_message)
        logger.warning(test_message)
        logger.error(test_message)

        # Verify log file exists and contains messages
        self.assertTrue(os.path.exists(self.test_log_file))
        with open(self.test_log_file, 'r') as f:
            content = f.read()
            # Verify INFO and higher level messages are present
            self.assertIn("INFO", content)
            self.assertIn("SUCCESS", content)
            self.assertIn("WARNING", content)
            self.assertIn("ERROR", content)
            # Verify DEBUG messages are NOT present
            self.assertNotIn("DEBUG", content)
            self.assertIn(test_message, content)
        
    def _test_debug_log_level(self):
        # Create logger with DEBUG level
        logger = Logger("TestLogger", log_level=logging.DEBUG, log_path=self.test_log_file)
        test_message = "Test message"
        
        # Log messages at different levels
        logger.debug(test_message)
        logger.info(test_message)
        logger.success(test_message)
        logger.warning(test_message)
        logger.error(test_message)

        # Verify log file exists and contains messages
        self.assertTrue(os.path.exists(self.test_log_file))
        with open(self.test_log_file, 'r') as f:
            content = f.read()
            # Verify all log levels are present including DEBUG
            self.assertIn("DEBUG", content)
            self.assertIn("INFO", content)
            self.assertIn("SUCCESS", content)
            self.assertIn("WARNING", content)
            self.assertIn("ERROR", content)
            self.assertIn(test_message, content)

if __name__ == '__main__':
    unittest.main()
