import os

from bullish import constants

__version__ = "0.0.2"

for path in list(constants.PATHS.values()):
    if not os.path.exists(path):
        os.mkdir(path)
