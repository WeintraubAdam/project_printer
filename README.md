# project_printer
All files &amp; docs for Pinnacle's summer project_printer

Project Documentation
---------------------------------------------------------------------------------------------------------------------------------------------------------
**config.py
**
Module Overview
The config.py file is responsible for managing and storing configuration settings used across the project. It centralizes the configuration variables to ensure consistency and ease of maintenance. This file allows to easily adjust settings without needing to alter the core logic within the other modules. Currently the uploaded files contain a mix of recent Mac pathways I used for testing, along with windows pathways that correspond to the desktop in the Print Shop. These need to be updated with changes, and will be added to with future use. For example, the ‘noDownload’ dictionary should continue to grow. 

Key Variables
•	CHROMEDRIVER_PATH: Specifies the path to the ChromeDriver executable. This is critical for Selenium WebDriver operations and will be different on every machine.
•	noDownload: As referenced through the rejected_file_process.py function, this dictionary contains the design_IDs of orders that should not be processed (for example windowed envelopes) .
•	sortDict: This dictionary contains all of the pathways to the corresponding hot folders on the local desktop. The Key is created later in the sorting_manager.py file, and if it matches the pathway is used to send the processed order.

Code Management Notes
•	Configuration Changes: When updating paths, URLs, or other settings, ensure that all dependent modules reflect these changes. For example, updating the CHROEMDRIVER_PATH will require verification that the path exists and is accessible.

--------------------------------------------------------------------------------------------------------------------------------------------------------- 
**main.py
**
Module Overview
The main.py file serves as the entry point for the project. It orchestrates the execution of various modules, coordinating the workflow from setup to completion along with passing Order objects to and from required files. It does basic sorting/filtering but mainly runs functions across files. 

Key Functions
•	if len(sys.argv) > 1: When this entire codebase was being created it initially relied on Google Cloud’s Pub/Sub service which would have to launch and host locally where it would monitor a gmail inbox and send notifications when new mail is received. Since this was not running 24/7 I implemented a way for it to record incoming mail outside of business hours, get a count and then send that to the main file as a line argument. Using this the file would run that many times (i.e. if 5 orders were placed outside of hours, when the script was first launched it would run and process the first 5 orders). Since this is no longer a use requirement the ‘download_count’ can technically be removed and rebuilt, but I have left it in as it can still be useful. 
•	Pronoun_callback: Currently for all MWT business cards the artwork contains a pronoun field that, if left empty, propogates with some default text. This callback is used in the selenium_order_manager to both hold its place in the function, but also to pass the current driver instance, and URL used to edit so that it may continue into the pronoun_manager file.
•	Orders = …: Here is the actual processing line that calls the selenium_order_manager function and gathers all orders it creates before sorting into either the noDownload dictionary and recording as a JSON, or passing into the sorting file.

Interdependencies
•	config.py: Loads configuration settings.
•	webdriver_setup.py: Sets up the Selenium WebDriver.
•	selenium_pronoun_manager.py: Manages the pronoun processing workflow.
•	Selenium_order_manager.py: Manages and gathers all processed Orders. 

Workflow Overview
1.	Initialization: Loads configuration and initializes logging.
2.	Driver Setup: Sets up the Selenium WebDriver.
3.	Order Processing: Manages the processing of orders, including pronoun editing.
  1.	Selenium_order_manager: Processes orders
  2.	Selenium_pronoun_manager: If MWT, handle pronoun exceptions
  3.	Return to Main sorting
    1.	Rejected_file_process: If rejeceted, format for JSON upload to local file
    2.	Sorting_manager: If valid, pass object to sorting

Error Handling
Not much error handling is needed for main as it largely calls the entire functions, but handling is passed larger scale such as the driver failing. 

---------------------------------------------------------------------------------------------------------------------------------------------------------
**selenium_pronoun_manager.py
**
Module Overview
The selenium_pronoun_manager.py file handles the editing of the pronoun within specifically MWT placed orders. It interacts with the web application to identify and modify the relevant field using independent functions. There is a specific order in which functions most process and navigate the webpage, which is also how they are laid out. It is also laid out in this manner as the URL technically is that of a pop-up window, not a separate page so how it interacts is more volatile to searching techniques. 

Key Functions 
•	switch_to_iframe: The first function and most important helps to initialize the location the other functions will work within as they all use some variation of xpath, css, or html searching for elements.
•	find_and_click_tab: Using CSS to find the tab elements this locates the 2nd element I believe before clicking the element. 
•	clear_pronoun_field_if_default: Most importantly as you can tell by the name, here is where it checks if the field has a current value of "Enter your pronouns or leave blank" before either filling with an empty value or not doing anything but logging.
•	process_pronouns: Here is the main function that using the passed along URL opens it and uses all the above mentioned functions to process the pronoun field for a required MWT business card before finishing and resuming back in selenium_order_manager.

Code Management Notes
Ensure that the web elements identified by this module remain stable; if the webpage changes, selectors may need to be updated. Regular updates may be required to keep the module compatible with the web application's structure.

Workflow Integration
This module is called after an initial Order object has been created and it is in the middle of gathering and recording information pertinent to each OrderItem line item. If a specific Order contains an OrderItem of MWT then this will automatically launch and use the edit_url gathered.

Error Handling
In every function there is a large amount of error handling detailing what is finding before navigating to/or from it. From this you are able to determine if one of the HTML elements has changed or been relocated just from what the logging returns to you. 

---------------------------------------------------------------------------------------------------------------------------------------------------------
**sorting_manager.py
**
Module Overview
The sorting_manager.py file manages the sorting logic for the downloaded files, organizing them based on the corresponding dictionary before moving locally.

Key Functions
•	move_file(): Creates a basic key from important OrderItems that are then used against a dictionary. If this key exists in the dictionary, the corresponding value returned will be the exact pathway to the HotFolder which it then sends it to.

Workflow Integration
This module is called after files are downloaded and an Order is technically finished, ready for local processing. To ensure they are properly organized it has the original download pathway along with other important Order and OrderItem values. 
Customization Notes
The sorting criteria are defined within this module. If additional criteria need to be added, they should be integrated here, and all dependent modules should be checked for compatibility.

---------------------------------------------------------------------------------------------------------------------------------------------------------
**webdriver_setup.py
**
Module Overview
The webdriver_setup.py file is responsible for configuring and initializing the Selenium WebDriver, including options and paths. Using the provided pathway this just returns a singular ‘driver’ instance that you see gets passed along to other functions and files. 

Key Functions
•	setup_driver(): Initializes the WebDriver with specified options. Most of the setup is code pulled from their available documentation with some added steps for error handling.

Interdependencies
•	config.py: Utilizes configuration settings for driver paths and options, if errors arise the pathway here should be checked to confirm it still is correct.
•	main.py: Called by the main function to set up the WebDriver.

Code Management Notes
Adjustments to WebDriver settings or paths should be done through config.py to ensure consistency. Changes in WebDriver versions or browser configurations should be documented and tested across all dependent modules.

---------------------------------------------------------------------------------------------------------------------------------------------------------
**selenium_order_manager.py
**
Module Overview
The selenium_order_manager.py file handles the management of orders within the web application, including navigating through the site and interacting with various elements to record valuable information. 

Methods
•	process_order(order): Processes an individual order, including navigating to the necessary pages and performing actions. This is the most important method in the entire codebase as this is where directly everything is handled. This follows the workflow from opening the page, logging in, opening HTML elements and gathering all relevant OrderItem line items. Within this you can see a for loop (this is where the count previously mentioned in main is referenced) that will gather as many total Orders are specified. The second nested for loop is where it handles a singular Order containing numers OrderItem orders, for example WSF will typically place an order containing numerous different business card orders. This second for loop will gather all information independent one another before wrapping it into the 1 Order. Within this second loop si where it also sorts for or activates the pronoun-manager. After everything is recorded and processed it will download the OrderItems and pass them along to wherever they are required.
•	navigate_to_orders: This is responsible for using the driver to open the webpage.
•	extract_pk_value: This is a static method that using a filename can extract the quantity of the pack from the name. This is used and referenced across the OrderItem.

Workflow
1.	Webpage Navigation: Opens and navigates through webpages.
2.	Order Navigation: Opens the correct dropdown tab that contains an Order OrderItems
3.	Order Processing: Executes the steps required to process the order, including editing and saving changes.
  1.	Pronoun Manager: If applicable will be activated here
  2.	Extract_pk_value: Always runs during processing for each OrderItem
4.	Order Download: Lastly downloads all relevant OrderItems and passes for handling.

Interdependencies
•	main.py: Called by the main function to gather all instances of the Order objects gathered. If an error occurs or it cannot create the object, then the workflow will stop short of any sorting.

Error Handling
Similar to the pronoun_manager, a lot of this and selenium is used navigating through CSS, HTML or xpath which can be very annoying and often times changes with the webpage. There is a lot of error handling for both locating the element and printing what value can be extracted from each element. This is very useful when first navigating through the elements (can be seen through inner <tr> work for example) to find an error as I have already seen the webpage change and need a new updated xpath. Additionally the file will log all values extracted as they are assigned to the object to double check everything functions as it is supposed to.

---------------------------------------------------------------------------------------------------------------------------------------------------------
**order.py
**
Module Overview
The order.py file defines the Order and OrderItem classes, which encapsulate the details of each order and its items. These classes form the core data structures used across the project for handling and processing orders.

Key Classes
•	Order: Represents a customer order, containing attributes such as order_id, company_id, and a list of OrderItem objects. The Order acts as the parent as an Order can contain numerous OrderItem instances.
•	OrderItem: Represents an item within an order, including attributes like design_id, file_name, file_path, qty, pk_qty, total_qty, and edit_url.

Code Management Notes
These classes are central to the data structure of the project. Any changes here will affect all modules that interact with orders. When modifying attributes or methods, ensure that all dependent modules are updated accordingly, and thoroughly test to prevent cascading issues. 

---------------------------------------------------------------------------------------------------------------------------------------------------------
**rejected_file_process.py
**
Module Overview
The rejected_file_process.py file handles the processing of files that have been rejected, ensuring they are managed and logged appropriately. It provides a mechanism to log rejections in a locally stored JSON file.

Key Functions
•	save_order_to_file(): There is no validating required as the Order object needing to be skipped over and logged will be directly passed into this object. This is not called or noted until after the selenium_order_manager has completed its entire function and processing. This function merely formats important fields for JSON before opening the local file, recording into it, saving and exiting.

Workflow
This function as mentioned can only be called from main after the entire selenium_order_manager has done its job of processing every order. As it is handling orders to be sent for sorting, it has the chance to be sent here instead. 

Interdependencies
•	main.py/selenium_order_manager: As mentioned this function fully relies on a completed Order object being passed into and from main, so any issues that arise there will cause this to not function as intended. 

Customization Notes
The criteria for rejecting files can be customized here. When new rejection criteria are introduced, ensure that they align with the overall project requirements and are consistently applied across all relevant modules.

---------------------------------------------------------------------------------------------------------------------------------------------------------
**Interdependencies and Workflows
**
Overall Project Workflow
1.	Initialization (config.py, main.py): Loads settings and initializes the environment. This includes configuring paths, URLs, and logging levels that the rest of the project relies on.
2.	Data Structure (order.py): Defines the core data structures used throughout the project. The Order and OrderItem classes provide the foundation upon which the entire workflow operates.
3.	Driver Setup (webdriver_setup.py): Configures and initializes the Selenium WebDriver, which is necessary for all subsequent Selenium operations.
4.	Order Processing (selenium_order_manager.py, selenium_pronoun_manager.py): Manages the processing of orders, including specific workflows like pronoun editing and overall order management.
5.	File Management (sorting_manager.py, rejected_file_process.py): Sorts and processes files, handling rejections as needed. These modules ensure that files are organized correctly and that any issues with files are handled systematically.

Interdependencies
•	config.py: Centralizes settings used across the project, ensuring that all modules operate with consistent configurations.
•	main.py: Orchestrates the entire workflow, interacting with all other modules and ensuring that each step in the process is executed in the correct order.
•	webdriver_setup.py: Provides the WebDriver setup for all Selenium operations, making it a critical dependency for any module that requires web interaction.
•	selenium_order_manager.py, selenium_pronoun_manager.py: Manage specific aspects of order processing and editing, relying on the WebDriver and configuration settings to function correctly.
•	sorting_manager.py, rejected_file_process.py: Handle the file sorting and error management processes, ensuring that files are correctly managed and that issues are logged and handled appropriately.

![image](https://github.com/user-attachments/assets/ba2bae0d-9f9c-497c-9f91-d6f6e2619f3a)
