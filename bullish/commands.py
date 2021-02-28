import os 
from pathlib import Path 

import click

from bullish import util, constants

###########################################################
# base bullish commands
###########################################################

@click.command()
@click.argument('tickers', nargs=-1)
@click.option('--num_dates', '-nd', required=False, type=int, default=0)
def fetch(tickers, num_dates):   
    
    tickers = list(tickers)

    if "watchlist" in tickers:
        tickers.remove("watchlist")
        with open(constants.Files.WATCHLIST, "r") as f:
                watchlist_tickers = [t.strip("\n") for t in f.readlines()]
        tickers += watchlist_tickers

    for ticker in tickers:
        print(ticker)
        ticker = ticker.upper()
        news = util.finviz_scrape(ticker)

        if not news:
            continue

        if num_dates > 0:
            news = util.trim_down_to_n_dates(news, int(num_dates))

        # Want the keys in reverse-chronological order from bottom up
        reverse_chron = list(news.keys())[::-1]
        print('')
        for rc in reverse_chron:
            print("-"*4+rc+"-"*4+ticker+"-"*92)

            for news_entry in news[rc]:
                print(f"{news_entry[0]}\n\t{news_entry[1]}")
            print('')


###########################################################
# bullish watchlist commands
###########################################################

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