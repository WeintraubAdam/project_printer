import os
import sys
import logging
import selenium_order_manager
import selenium_pronoun_manager
import sorting_manager
import config
import webdriver_setup
import rejected_file_process 

def pronoun_callback(driver, edit_url):
    pronoun_mgr = selenium_pronoun_manager.PronounManager(driver)
    pronoun_mgr.process_pronouns(edit_url)


def main():
    # Initializing local variables from config paths to be passed around and used within functions across files
    printlane_url = config.PRINTLANE_URL
    download_path = config.DOWNLOAD_PATH
    driver_path = config.CHROMEDRIVER_PATH


    log_file_path = config.LOG_FILE_PATH

    # Driver setups
    driver = webdriver_setup.setup_driver(driver_path)

    manager = selenium_order_manager.OrderManager( printlane_url, download_path, driver_path, driver, wait_time=5)
    

    if len(sys.argv) > 1:
        download_count = int(sys.argv[1])
    else:
        download_count = 1

    # Small test to verify driver setup and navigation
    try:
        wait = manager.navigate_to_orders()
        logging.info("Driver setup and navigation test passed.")
    except Exception as e:
        logging.error(f"Test failed: {e}")

    Orders = manager.process_orders(download_count, pronoun_callback)
    for order in Orders:
        for item in order.items:
            if item.design_id in config.noDownload:
                logging.info("orderItem in no download list, will not download and add to log")
                # Call the save_order_to_file function from order_utils
                rejected_file_process.save_order_to_file(order, log_file_path)
            else:
                sorting_manager.move_file(item, order.company_id)

if __name__ == "__main__":
    main()
