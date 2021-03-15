import time
from datetime import datetime
import os
import argparse 
import json

import bullish 
from bullish import constants
from bullish.util import util

def write_information():
    with open(constants.Files.WATCHLIST, "r") as f:
        watchlist_tickers = [t.strip("\n") for t in f.readlines()]

    with open(constants.Files.TEMP_DATA, "r+") as f:
        last_news = json.load(f)
        last_news_key = list(last_news.keys())[0]

    send_updates = False

    current_news_key = str(datetime.now().date())
    current_news = {current_news_key : {}}
    diff = {}
    for ticker in watchlist_tickers:
        ticker = ticker.upper()
        current_ticker_news = util.finviz_scrape(ticker)
        current_ticker_news = list(util.trim_down_to_n_dates(current_ticker_news, 1).values())[0]

        if ticker in last_news[last_news_key].keys():
            last_ticker_news = last_news[last_news_key][ticker]
        else:
            current_news[current_news_key][ticker] = current_ticker_news
            diff[ticker] = current_ticker_news
            send_updates = True
            continue

        current_ticker_news_headlines = [h[0] for h in current_ticker_news]
        last_ticker_news_headlines = [h[0] for h in last_ticker_news]
        diff_content = [current_ticker_news[i] for i, h in enumerate(current_ticker_news_headlines) if h not in last_ticker_news_headlines]
        current_news[current_news_key][ticker] = current_ticker_news

        if len(diff_content):
            diff[ticker] = diff_content
            send_updates = True

    with open(constants.Files.TEMP_DATA, "w+") as f:
        json.dump(current_news, f, indent = 2)

    if send_updates:
        diff_test_name = str(datetime.now()).split(".")[0].replace(":", "-").replace(" ", "-")
        with open(constants.Files.DIFF_TEST.format(diff_test_name), "w+") as f:
            json.dump(diff, f, indent=2)

def start_process(parent_process_pid):
    

    while True:
        write_information()

        # For keeping track of when the program is running
        with open("C:/Users/HP/_projects/bullish/pid.txt", "w") as f:
            f.write(str(datetime.now()) + "\n")

        seconds = 60*10 # Run this often
        time.sleep(seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('parent')
    args = parser.parse_args()
    start_process(args.parent)
