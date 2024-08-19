import os

PRINTLANE_URL = os.getenv("PRINTLANE_URL", "https://studio.printlane.com/login?to=%252F5fa41117d6f02e001010eb95%252Forders")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/Users/adam.weintraub/Downloads") 

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/Users/MacbookRetina/.wdm/drivers/chromedriver/mac64/127.0.6533.119/chromedriver-mac-x64/chromedriver")
# CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", r"C:\\Users\\press\\.wdm\\drivers\\chromedriver\\win64\\126.0.6478.126\\chromedriver.exe")


LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/Users/MacbookRetina/Desktop/project_printer_FINAL/do_not_process_LOGS/order_history.txt")
DO_NOT_PROCESS = os.getenv("DO_NOT_PROCESS", "/Users/MacbookRetina/Desktop/project_printer_FINAL/do_not_process_LOGS")
# LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", r"C:\Users\press\OneDrive\Desktop\project_printer\do_not_process_LOGS\order_history.txt")
# DO_NOT_PROCESS = os.getenv("DO_NOT_PROCESS", r"C:\Users\press\OneDrive\Desktop\project_printer\do_not_process_LOGS")


# Replace with your username and password
USERNAME_PL = "Chris.Whelan@pinnaclepromotions.com"
PASSWORD_PL = "Scockett061786$"


# design_ID that shouldn't be processed
noDownload = [
    "2792",
    "2753",
    "2748"
]


sortDict = {
    "mwt_qty50" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty50",
    "mwt_qty100" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty100",
    "mwt_qty150" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty150",
    "mwt_qty200" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty200",
    "mwt_qty250" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty250",
    "mwt_qty300" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty300",
    "mwt_qty350" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty350",
    "mwt_qty400" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty400",
    "mwt_qty450" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty450",
    "mwt_qty500" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty500",
    
    "wil_qty50" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty50",
    "wil_qty100" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty100",
    "wil_qty150" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty150",
    "wil_qty200" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty200",
    "wil_qty250" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty250",
    "wil_qty300" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty300",
    "wil_qty350" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty350",
    "wil_qty400" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty400",
    "wil_qty450" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty450",
    "wil_qty500" : r"C:\Users\press\OneDrive\Desktop\HotFolders\MWT_WIL\Qty500",


    "lge_qty50" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty50",
    "lge_qty100" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty100",
    "lge_qty150" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty150",
    "lge_qty200" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty200",
    "lge_qty250" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty250",
    "lge_qty300" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty300",
    "lge_qty350" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty350",
    "lge_qty400" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty400",
    "lge_qty450" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty450",
    "lge_qty500" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty500",

    "wsf_qty50" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty50",
    "wsf_qty100" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty100",
    "wsf_qty150" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty150",
    "wsf_qty200" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty200",
    "wsf_qty250" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty250",
    "wsf_qty300" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty300",
    "wsf_qty350" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty350",
    "wsf_qty400" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty400",
    "wsf_qty450" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty450",
    "wsf_qty500" : r"C:\Users\press\OneDrive\Desktop\HotFolders\WSF_LGE\Qty500",
}