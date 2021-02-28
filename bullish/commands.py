import os 
from pathlib import Path 

import click

from bullish import util, constants

###########################################################
# base bullish commands
###########################################################

@click.command()
@click.argument('ticker')
@click.option('--num_articles', '-na', required=False, type=int, default=0)
def fetch(ticker, num_articles):
    news = util.finviz_scrape(ticker)

    if num_articles > 0:
        news = util.trim_down_to_n_dates(all_news, int(num_articles))

    # Want the keys in reverse-chronological order from bottom up
    reverse_chron = list(news.keys())[::-1]
    print('')
    for rc in reverse_chron:
        print("-"*4+rc+"-"*120)

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
@click.argument('ticker')
def add(ticker):
    if not os.path.exists(constants.Files.WATCHLIST):
       Path(constants.Files.WATCHLIST).touch()

    with open(constants.Files.WATCHLIST, "r") as f:
        watchlist = [t.strip("\n") for t in f.readlines()]

    if ticker not in watchlist:
        watchlist.append(ticker.upper())
    else:
        print(f"{ticker.upper()} already exists in watchlist")
        return

    watchlist = sorted(watchlist)

    with open(constants.Files.WATCHLIST, "w+") as f:
        f.write('\n'.join(watchlist))
    
    print(f"{ticker.upper()} added to watchlist")