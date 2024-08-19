import os
import shutil
import logging
from config import sortDict

# Setup logging for debugging and tracking script execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def move_file(OrderItem, comp_id):
    """
    Moves the file based on matching location in dictionary
    Takes arguments from order and if they appear in dictionary, move based on pathway as key response
    
    Args:
        order_item (OrderItem): The order item object containing file and order details.
    """
    try:
        # Extract necessary information from the order_item object
        file_name = OrderItem.file_name
        file_path = OrderItem.file_path
        total_qty = str(OrderItem.total_qty)

        company_id = comp_id

        
        sortDictKey = f"{company_id.lower()}_qty{total_qty}"

        if sortDictKey in sortDict:
            logging.info(f"{sortDictKey} found in dictionary")
            new_file_path = os.path.join(sortDict[sortDictKey], file_name)
            shutil.move(file_path, new_file_path)
            logging.info(f"File moved to {new_file_path}")
        else:
            logging.info(f"Error, did not move file")


    except Exception as e:
        logging.error(f"An error occurred while moving the file: {str(e)}")
