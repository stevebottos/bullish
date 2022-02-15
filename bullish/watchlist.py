import os
from pathlib import Path
from datetime import datetime
import json

import click
import colorama

colorama.init()

from bullish.util import util
from bullish import constants
from bullish.constants import STYLES
from bullish.alerts import update_subscribe


def server_watchlist_update():
    with open(constants.Files.USER_EMAIL) as f:
        email = f.read()
    update_subscribe(email)


@click.command()
def ls():
    if os.path.exists(constants.Files.WATCHLIST):
        with open(constants.Files.WATCHLIST, "r") as f:
            watchlist = [
                t.strip("\n") for t in f.readlines()
            ]  # Removing then re-adding new lines below to avoid weird spaces
            print(*watchlist, sep="\n")
    else:
        print(
            'No watchlist exists. Use "bullish watchlist add <ticker>" to create one.'
        )


@click.command()
@click.argument("tickers", nargs=-1)
def add(tickers):

    if not os.path.exists(constants.Files.WATCHLIST):
        Path(constants.Files.WATCHLIST).touch()

    if not os.path.exists(constants.Files.NOTES):
        with open(constants.Files.NOTES, "w+") as f:
            placeholder = {}
            json.dump(placeholder, f)

    if not os.path.exists(constants.Files.TEMP_DATA):
        with open(constants.Files.TEMP_DATA, "w+") as f:
            rn = str(datetime.now().date())
            placeholder = {rn: {}}
            json.dump(placeholder, f)

    with open(constants.Files.WATCHLIST, "r") as f1, open(
        constants.Files.NOTES, "r"
    ) as f2:
        watchlist = [t.strip("\n") for t in f1.readlines()]
        notes = json.load(f2)

    for ticker in tickers:
        ticker = ticker.upper()

        if ticker not in watchlist:
            watchlist.append(ticker)
            print(f"{ticker} added to watchlist")

            watchlist = sorted(watchlist)
            with open(constants.Files.WATCHLIST, "w+") as f1, open(
                constants.Files.NOTES, "w+"
            ) as f2:

                f1.write("\n".join(watchlist))
                notes[ticker] = constants.NOTES_FIELDS
                notes = dict(sorted(notes.items(), key=lambda item: item[0]))
                f2.write(json.dumps(notes, indent=2))

        else:
            print(f"{ticker} already exists in watchlist")
            continue

    if os.path.exists(constants.Files.USER_EMAIL):
        server_watchlist_update()


@click.command()
@click.argument("tickers", nargs=-1)
def remove(tickers):
    if not os.path.exists(constants.Files.WATCHLIST):
        print(
            'No watchlist exists. Use "bullish watchlist add <ticker>" to create one.'
        )
        return

    with open(constants.Files.WATCHLIST, "r") as f1, open(
        constants.Files.NOTES, "r"
    ) as f2:
        watchlist = [t.strip("\n") for t in f1.readlines()]
        notes = json.load(f2)

    for ticker in tickers:
        ticker = ticker.upper()

        if ticker in watchlist:
            watchlist.remove(ticker)

            watchlist = sorted(watchlist)
            with open(constants.Files.WATCHLIST, "w+") as f1, open(
                constants.Files.NOTES, "w+"
            ) as f2:

                f1.write("\n".join(watchlist))
                del notes[ticker]
                notes = dict(sorted(notes.items(), key=lambda item: item[0]))
                f2.write(json.dumps(notes, indent=2))
        else:
            print(f"{ticker} does not exist in watchlist")
            continue

    print(f"{ticker} removed from watchlist")

    if os.path.exists(constants.Files.USER_EMAIL):
        server_watchlist_update()
