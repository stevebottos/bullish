import os 
from pathlib import Path 
from datetime import datetime 

import click
import colorama
colorama.init()

from bullish import util, constants
from bullish.constants import STYLES

@click.command()
def ls():
    if os.path.exists(constants.Files.WATCHLIST):
        with open(constants.Files.WATCHLIST, "r") as f:
            watchlist = [t.strip("\n") for t in f.readlines()] # Removing then re-adding new lines below to avoid weird spaces
            print(*watchlist, sep="\n")
    else:
        print("No watchlist exists. Use \"bullish watchlist add <ticker>\" to create one.")


@click.command()
@click.argument('tickers', nargs=-1)
def add(tickers):
    if not os.path.exists(constants.Files.WATCHLIST):
       Path(constants.Files.WATCHLIST).touch()

    with open(constants.Files.WATCHLIST, "r") as f:
        watchlist = [t.strip("\n") for t in f.readlines()]

    for ticker in tickers:
        ticker = ticker.upper()

        if ticker not in watchlist:
            watchlist.append(ticker)
            print(f"{ticker} added to watchlist")
        else:
            print(f"{ticker} already exists in watchlist")
            continue

    watchlist = sorted(watchlist)
    with open(constants.Files.WATCHLIST, "w+") as f:
        f.write('\n'.join(watchlist))
    

@click.command()
@click.argument('tickers', nargs=-1)
def remove(tickers):
    if not os.path.exists(constants.Files.WATCHLIST):
       print("No watchlist exists. Use \"bullish watchlist add <ticker>\" to create one.")

    with open(constants.Files.WATCHLIST, "r") as f:
        watchlist = [t.strip("\n") for t in f.readlines()]

    for ticker in tickers:
        ticker = ticker.upper()

        if ticker in watchlist:
            watchlist.remove(ticker)
        else:
            print(f"{ticker} does not exist in watchlist")
            continue

    watchlist = sorted(watchlist)
    with open(constants.Files.WATCHLIST, "w+") as f:
        f.write('\n'.join(watchlist))
    
    print(f"{ticker} removed from watchlist")