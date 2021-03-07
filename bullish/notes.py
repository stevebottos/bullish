import os 
import json
from datetime import datetime

import yaml 
import click

from bullish.util import util
from bullish import constants
from bullish.constants import STYLES

@click.command()
def ls():
    if os.path.exists(constants.Files.NOTES):
        with open(constants.Files.NOTES, "r") as f:
            notes = json.load(f)
            
            for ticker in notes:
                print(STYLES.GREEN+STYLES.BOLD+"--------"+ticker+STYLES.END)
                print(yaml.dump(notes[ticker], allow_unicode=True, default_flow_style=False))
    else:
        print("You don't have any notes yet! To get started, use \"bullish watchlist add <ticker>\" to create a watchlist. You'll then be able to start adding notes for that ticker.")


@click.command()
@click.argument('ticker', nargs=1)
@click.argument('field', nargs=1)
def update(ticker, field):
    ticker = ticker.upper()

    if not os.path.exists(constants.Files.NOTES):
        print("You don't have any notes yet! To get started, use \"bullish watchlist add <ticker>\" to create a watchlist. You'll then be able to start adding notes for that ticker.")
        return
    
    with open(constants.Files.NOTES, "r") as f:
            notes = json.load(f)
    
    if ticker not in notes:
        print(f"{ticker} is not in your watchlist. Use \"bullish watchlist add <ticker>\" to add it.")
        return

    if field not in notes[ticker]:
        acceptable_fields = ", ".join([f.lower() for f in notes[ticker]])
        print(f"{field} is not an editable field. Choose from:\n\t{acceptable_fields}")
        return

    editing = notes[ticker][field]

    

