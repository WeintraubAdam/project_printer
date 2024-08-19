import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging to display timestamps and log levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PronounManager:
    def __init__(self, driver):
        self.driver = driver

    def switch_to_iframe(self, iframe_xpath):
        """
        Switch to the iframe specified by the given XPath.
        
        Args:
            iframe_xpath: The XPath string of the iframe to switch to.
        """
        try:
            iframe = self.driver.find_element(By.XPATH, iframe_xpath)
            self.driver.switch_to.frame(iframe)
            logging.info("Switched to the iframe.")
        except Exception as e:
            logging.error(f"Error switching to iframe: {e}")

    def find_and_click_tab(self):
        """
        Find and click the specified tab element using CSS selector.
        """
        try:
            tab_css_selector = '#app > div > div > div.app__content > div.navbar > div.navbar__tabs > div.navbar__list > div:nth-child(2) > div > div'
            tab_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tab_css_selector)))
            self.driver.execute_script("arguments[0].click();", tab_element)
            logging.info("Clicked on the tab element using CSS Selector and JavaScript.")
            time.sleep(2)  # Wait for 2 seconds for the tab to be fully loaded
        except Exception as e:
            logging.error(f"Tab element not found: {e}")

    def clear_pronoun_field_if_default(self):
        """
        Clear the pronoun field if it contains the default text.
        """
        try:
            pronoun_fields = self.driver.find_elements(By.CLASS_NAME, 'pit__input')
            for field in pronoun_fields:
                current_value = field.get_attribute("value")
                logging.info(f"Current value of the field: {current_value}")
                if current_value == "Enter your pronouns or leave blank":
                    self.driver.execute_script("arguments[0].value = '';", field)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
                    time.sleep(1)  # Ensure the clear action is processed
                    updated_value = field.get_attribute("value")
                    logging.info(f"Updated value of the field after clearing: {updated_value}")
                    if updated_value == "":
                        logging.info("Cleared the pronoun field successfully.")
                    else:
                        logging.warning("Failed to clear the pronoun field.")
                    break
            else:
                logging.info("Pronoun field does not contain the default text.")
        except Exception as e:
            logging.error(f"Pronoun field not found or another error occurred: {e}")

    def click_save_button(self):
        """
        Click the save button on the page.
        """
        try:
            save_button_xpath = '//button[@class="pbtn pbtn--primary pbtn--nowrap pbtn--lg"]'
            save_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, save_button_xpath)))
            self.driver.execute_script("arguments[0].click();", save_button)
            logging.info("Clicked the save button.")
            time.sleep(10)  # Wait to ensure the save process completes
        except Exception as e:
            logging.error(f"Save button not found or another error occurred: {e}")

    def process_pronouns(self, url):
        """
        Process the pronoun field in the specified URL.
        Uses independent local functions to navigate across webpage to find pronoun field
        If text matches default then replace with empty string and save for new processing download

        Args:
            url: The URL to navigate to.
        """
        logging.info(f"Starting pronoun processing with URL: {url}")
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logging.info("Opened a new tab and switched to it.")

        try:
            self.driver.get(url)
            logging.info(f"Navigated to URL: {url}")
            time.sleep(2)  # Pause for observation

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            logging.info("Element found: body")
            time.sleep(2)  # Pause for observation

            self.switch_to_iframe("//iframe[@class='colorlab-wrapper__frame']")
            self.find_and_click_tab()
            self.clear_pronoun_field_if_default()
            self.click_save_button()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            logging.info("Closed the new tab and switched back to the original tab.")
            logging.info("Pronoun processing completed.")
