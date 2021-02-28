import os
ROOT = "bullish"

PATHS = {
    "data_dir": os.path.join(ROOT, "data")
}

class Files:
    WATCHLIST = os.path.join(PATHS["data_dir"], "watchlist")