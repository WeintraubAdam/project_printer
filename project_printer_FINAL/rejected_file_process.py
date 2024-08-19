import json
from pathlib import Path
from datetime import datetime
import shutil
import config
import logging

# Setup logging for debugging and tracking script execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_order_to_file(order, file_path):
    """
    Saves the given order to a text file in JSON format, prepending it to keep the newest entries at the top.
    """


    for item in order.items:
        # move to log directory
        shutil.move(item.file_path, config.DO_NOT_PROCESS)
        item.file_path = f"{config.DO_NOT_PROCESS}/{item.file_name}"
        logging.info(f"Moving file to do not process directory")


    # Serialize the order to a dictionary
    order_dict = {
        "order_id": order.order_id,
        "company_id": order.company_id,
        "items": [item.__dict__ for item in order.items],
        "created_at": datetime.now().isoformat()
    }
    
    # Read the existing file content
    file = Path(file_path)
    if file.exists():
        with file.open('r') as f:
            logging.info(f"found and opening log file")
            existing_data = json.load(f)
    else:
        existing_data = []
    
    # Prepend the new order data
    existing_data.insert(0, order_dict)
    
    # Write the updated content back to the file
    with file.open('w') as f:
        json.dump(existing_data, f, indent=4)
        logging.info(f"Adding new JSON data for log")

