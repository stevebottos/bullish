import os 
from datetime import datetime 

import click
import colorama
colorama.init()

from bullish import util, constants
from bullish.constants import STYLES
   
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

        ticker = ticker.upper()
        news = util.finviz_scrape(ticker)

        if not news:
            continue

        if num_dates > 0:
            news = util.trim_down_to_n_dates(news, int(num_dates))

        # Want the keys in reverse-chronological order from bottom up
        reverse_chron = list(news.keys())[::-1]

        for rc in reverse_chron:
            print(STYLES.YELLOW + STYLES.BOLD + "-"*4+rc+"-"*4+ticker+"-"*92 + STYLES.END)

            for news_entry in news[rc]:
                print(STYLES.GREEN + STYLES.BOLD + f"  {news_entry[0]}\n" + STYLES.END +
                STYLES.UNDERLINE + f"  {news_entry[1]}" + STYLES.END)
        print('')


@click.command()
@click.argument('tickers', nargs=-1)
@click.option('--num_dates', '-nd', required=False, type=int, default=0)
def report(tickers, num_dates):   
    
    tickers = list(tickers)

    if "watchlist" in tickers:
        tickers.remove("watchlist")
        with open(constants.Files.WATCHLIST, "r") as f:
            watchlist_tickers = [t.strip("\n") for t in f.readlines()]
        tickers += watchlist_tickers

    fname = str(datetime.now()).split(".")[0]
    fname = fname.replace(" ", "_").replace(":", "-")

    with open(constants.Files.REPORT.format(fname), "w+") as f:
        for ticker in tickers:

            ticker = ticker.upper()
            news = util.finviz_scrape(ticker)

            if not news:
                continue

            if num_dates > 0:
                news = util.trim_down_to_n_dates(news, int(num_dates))

            # Want the keys in reverse-chronological order from bottom up
            reverse_chron = list(news.keys())[::-1]

            for rc in reverse_chron:
                f.write("-"*4+rc+"-"*4+ticker+"-"*92+"\n")

                for news_entry in news[rc]:
                    f.write(f"  {news_entry[0]}\n  {news_entry[1]}\n")
            f.write('\n')