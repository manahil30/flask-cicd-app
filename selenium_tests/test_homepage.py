from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import unittest

class TestHomepage(unittest.TestCase):
    """Test Case 1: Homepage Functionality Test"""
    
    def setUp(self):
        """Setup - Runs before each test"""
        # Configure Chrome for headless mode (no GUI)
        chrome_options = Options()
        chrome_options.add_argument('--headless')      # No browser window
        chrome_options.add_argument('--no-sandbox')    # Required for Docker
        chrome_options.add_argument('--disable-dev-shm-usage')  # Prevent memory issues
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements
    
    def test_homepage_loads_successfully(self):
        """Test that homepage loads and shows welcome message"""
        # Navigate to the web application
        self.driver.get("http://webapp:5000")
        
        # Get page source and verify content
        page_source = self.driver.page_source
        
        # Assert that welcome message is present
        assert "Welcome" in page_source or "Flask" in page_source
        
        # Take screenshot for evidence
        self.driver.save_screenshot("homepage_test.png")
        
        print("✅ Homepage test passed!")
    
    def test_homepage_status(self):
        """Test that homepage returns successful response"""
        self.driver.get("http://webapp:5000")
        
        # Check that page loaded completely
        assert self.driver.execute_script("return document.readyState") == "complete"
        
        print("✅ Homepage status test passed!")
    
    def tearDown(self):
        """Cleanup - Runs after each test"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
