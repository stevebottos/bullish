import os

_PACKAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

ROOT = open(os.path.join(_PACKAGE_DIR, 'package_root'), 'r+').read()

PATHS = {
    "data_dir": os.path.join(ROOT, "data"),
    "reports_dir": os.path.join(ROOT, "reports")
}

class Files:
    WATCHLIST = os.path.join(PATHS["data_dir"], "watchlist")
    REPORT = os.path.join(PATHS["reports_dir"], "{}.txt")