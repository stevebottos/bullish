import os

_PACKAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ROOT = open(os.path.join(_PACKAGE_DIR, 'package_root'), 'r+').read()


PATHS = {
    "data_dir": os.path.join(ROOT, "data"),
    "reports_dir": os.path.join(ROOT, "reports")
}


class Files:
    WATCHLIST = os.path.join(PATHS["data_dir"], "watchlist.txt")
    NOTES = os.path.join(PATHS["data_dir"], "notes.json")
    REPORT = os.path.join(PATHS["reports_dir"], "{}.txt")
    TEMP_DATA = os.path.join(PATHS["data_dir"], "temp_data.json")
    DIFF_TEST = os.path.join(PATHS["data_dir"], "{}.json")

NOTES_FIELDS = {
    "Financials": None,
    "Catalysts": None,
    "Ideas": None
}


class STYLES:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'