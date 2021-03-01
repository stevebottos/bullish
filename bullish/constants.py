import os
ROOT = "bullish"

PATHS = {
    "data_dir": os.path.join(ROOT, "data"),
    "reports_dir": os.path.join(ROOT, "reports")
}

class Files:
    WATCHLIST = os.path.join(PATHS["data_dir"], "watchlist")
    REPORT = os.path.join(PATHS["reports_dir"], "{}.txt")