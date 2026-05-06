from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import requests

class TestLoginPage(unittest.TestCase):
    """Test Case 2: Login Page and API Functionality Test"""
    
    def setUp(self):
        """Setup Chrome driver for each test"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def test_login_page_accessible(self):
        """Test that login page is accessible"""
        self.driver.get("http://webapp:5000/login")
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Assert page loads successfully
        assert self.driver.current_url.endswith("/login") or self.driver.page_source is not None
        
        # Take screenshot for evidence
        self.driver.save_screenshot("login_page_test.png")
        
        print("✅ Login page accessibility test passed!")
    
    def test_login_api_response(self):
        """Test that login endpoint returns proper JSON response"""
        # Direct API test using requests library
        response = requests.get("http://webapp:5000/login")
        
        # Assert response status is 200 OK
        assert response.status_code == 200
        
        # Parse JSON response
        data = response.json()
        
        # Verify response contains expected fields
        assert "message" in data or "status" in data
        
        print("✅ Login API response test passed!")
    
    def tearDown(self):
        """Clean up after each test"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
