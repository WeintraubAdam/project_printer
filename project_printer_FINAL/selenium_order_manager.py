import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import config

from order import Order, OrderItem  # Import the Order and OrderItem classes from the new file

# Setup logging for debugging and tracking script execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrderManager:
    """
    Class to manage the order processing.
    """
    def __init__(self, url, download_path, driver_path, driver, wait_time=5):
            #self.user_profile_path = user_profile_path  # Path to the user profile
            self.url = url  # URL of the orders page
            self.download_path = download_path  # Path to the downloads folder
            self.driver_path = driver_path  # Path to the ChromeDriver executable
            self.driver = driver  # WebDriver instance
            self.wait_time = wait_time  # Time to wait for download to complete


    def navigate_to_orders(self):
        """
        Navigates to the orders page and returns a WebDriverWait object for further interactions.
        """
        self.driver.get(self.url)  # Navigate to the orders page
        wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds
        logging.info("Navigated to the orders page.")
        return wait

    @staticmethod
    def extract_pk_value(filename):
        """
        Extracts the integer value following 'pk' in a filename.
        """
        try:
            pk_position = filename.find('pk')  # Find 'pk' in the filename
            if pk_position == -1:
                raise ValueError("The string 'pk' was not found in the filename.")
            
            start = pk_position + 2  # Start after 'pk'
            end = start
            while end < len(filename) and not filename[end].isdigit():
                end += 1
            
            if end == len(filename):
                raise ValueError("No integer found after 'pk' in the filename.")
            
            start = end
            while end < len(filename) and filename[end].isdigit():
                end += 1
            
            return int(filename[start:end])  # Return the extracted integer
        except ValueError as e:
            logging.error(f"Error: {e}")
            return None

    def process_orders(self, count=1, callback=None):
        """
        Processes orders based on the given count.

         Parameters:
         - count (int): The number of orders to process. Defaults to 1.
         - callback (function): A callback function to process specific actions (e.g., pronoun editing) for certain orders. Defaults to None.
         
         Returns:
         - list: A list of processed Order objects.
        """
        wait = self.navigate_to_orders()  # Navigate to the orders page


        # Find and fill the username field
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your email address']")))
        username_field.send_keys(config.USERNAME_PL)

        # Find and fill the password field
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your password']")))
        password_field.send_keys(config.PASSWORD_PL)
        password_field.send_keys(Keys.RETURN)


        orders = []  # List to hold all orders

        for i in range(1, count + 1):  # Loop through the specified number of orders
            try:
                # Locate and click the toggle to expand the item
                div_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[@class='ptr__toggle'])[{i}]")))
                div_toggle.click()
                logging.info(f"Expanded order {i}.")

                # Extract the Order ID using the specific span and strong tags
                order_span = self.driver.find_element(By.XPATH, f"(//span[contains(@class, 'view--orders__column-id')])[{i}]")
                order_element = order_span.find_element(By.TAG_NAME, 'strong')
                order_id = order_element.text
                logging.info(f"Extracted Order ID: {order_id}")

                # For now, use order_id as company_id
                company_id = order_id[:3]
                logging.info(f"Extracted company ID: {company_id}")

                # Create an Order object
                order = Order(order_id, company_id)
                logging.info(f"Order Created: {order}")

                # Locate the <tr> element for the expanded order details
                inner_tr_xpath = "//tr[@class='ptabletr ptabletr--details']"
                inner_tr = self.driver.find_element(By.XPATH, inner_tr_xpath)
                logging.info(f"Found inner <tr> for order {i}.")

                # Locate the inner tbody for the line items within the expanded order details
                inner_tbody = inner_tr.find_element(By.XPATH, ".//tbody[@class='divide-y divide-gray-200']")
                logging.info(f"Found inner tbody for order {i}.")

                # Count the number of tr elements with class 'ptabletr' within the inner tbody
                line_items = inner_tbody.find_elements(By.CLASS_NAME, 'ptabletr')
                line_item_count = len(line_items)
                logging.info(f"Found {line_item_count} line items for order {order_id}.")

                for j in range(1, line_item_count + 1):  # Iterate over each line item
                    # Extract the Design ID from the href attribute
                    design_element = inner_tbody.find_element(By.XPATH, f"(//a[contains(@href, 'designs?id=')])[{j}]")
                    design_id = design_element.get_attribute("href").split('id=')[-1]
                    logging.info(f"Extracted design ID: {design_id}")

                    # Extract the quantity using the specific structure
                    qty_xpath = ".//td[contains(@class, 'ptc') and contains(@class, 'ptc--right')]"
                    qty_element = inner_tbody.find_element(By.XPATH, qty_xpath)           
                    qty = int(qty_element.text)
                    logging.info(f"Extracted Qty: {qty}")

                    # Setup edit_url for orderItem then run for 'mwt'
                    link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'designer.printlane.com') and contains(@href, 'clb-shop') and contains(@href, 'clb-id') and contains(@href, 'clb-token') and contains(@href, 'clb-language=en') and @class='block']")))
                            
                    # Get the href attribute of the link
                    edit_url = link.get_attribute('href')
                    logging.info(f"Got link href: {edit_url}")

                    # Check for if MWT run for pronouns
                    if 'mwt' in order.company_id.lower():
                        logging.info(f"found MWT")
                        if callback:
                            callback(self.driver, edit_url)
                    
                    # Verify the presence of the download button
                    download_button_xpath = f"(//button[contains(@data-breadcrumb, 'Download design')])[{j}]"
                    download_button = self.driver.find_element(By.XPATH, download_button_xpath)
                    logging.info(f"Download button for line item {j} is present.")

                    # Click the download button to download the file
                    download_button.click()
                    logging.info(f"Clicked the download button for line item {j}.")

                    # Wait for the download to complete (this should be adjusted based on download time)
                    time.sleep(self.wait_time)

                    # Get the file name from the downloads folder (assuming the most recent file is the one downloaded)
                    files = os.listdir(self.download_path)
                    files.sort(key=lambda x: os.path.getctime(os.path.join(self.download_path, x)), reverse=True)
                    file_name = files[0]
                    file_path = os.path.join(self.download_path, file_name)
                    logging.info(f"Downloaded file: {file_name}")

                    # Extract the pk_qty from the file name
                    pk_qty = self.extract_pk_value(file_name)
                    if pk_qty is None:
                        raise ValueError("Failed to extract pk_qty from the file name.")
                    logging.info(f"Extracted pk_qty: {pk_qty}")

                    # Calculate the total_qty
                    total_qty = qty * pk_qty
                    logging.info(f"Calculated total_qty: {total_qty}")
                    
                    # Initialize the OrderItem object
                    order_item = OrderItem(order_id, company_id, design_id, file_name, file_path, qty, pk_qty, total_qty, edit_url)
                    logging.info(f"OrderItem created: {order_item}")

                    # Add the OrderItem to the Order
                    order.add_item(order_item)

                # Add the order to the list of orders
                orders.append(order)
                logging.info(f"Order processed: {order.order_id} with line items: {len(order.items)}")

                div_toggle.click()  # Close the order pane

            except Exception as e:
                logging.error(f"Failed to download line item {i}: {str(e)}")
                continue

        self.driver.quit()  # Quit the driver after processing all items
        logging.info("Browser closed and script finished.")

        if orders:
            return orders
