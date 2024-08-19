import os
import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(driver_path):
    """
    Sets up the Chrome WebDriver with the specified user profile.

    Parameters:
    - driver_path (str): The path to the ChromeDriver executable.

    Returns:
    - WebDriver: An instance of Chrome WebDriver.
    """
    try:
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument(f"user-data-dir={user_profile_path}")  # Add user profile to options

        logging.info(f"Using ChromeDriver at: {driver_path}")

        # Check if the installed path points to an executable file
        if not os.path.isfile(driver_path):
            raise FileNotFoundError(f"ChromeDriver executable not found at: {driver_path}")

        # Set the executable permission if not already set
        if not os.access(driver_path, os.X_OK):
            os.chmod(driver_path, 0o755)
            logging.info(f"Set executable permissions for: {driver_path}")

        # Create the Service object
        service = Service(driver_path)
        logging.info(f"Service created with ChromeDriver at: {driver_path}")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Chrome WebDriver setup complete.")
        return driver
    
    except Exception as e:
        logging.error(f"An error occurred during WebDriver setup: {e}")
        logging.error("Detailed traceback:", exc_info=True)
        sys.exit(1)
