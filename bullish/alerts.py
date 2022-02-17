import os
import requests

import click

from server.constants import Server
from bullish.constants import Files


def update_subscribe(email):

    with open(Files.USER_EMAIL, "w+") as f1, open(Files.WATCHLIST) as f2:
        f1.write(email)
        watchlist = [ticker.rstrip("\n") for ticker in f2.readlines()]

    data = {"email": email, "watchlist": watchlist}
    res = requests.post(url=Server.URL + "/update_subscribe", json=data)


@click.command()
def health():
    res = requests.get(url=Server.URL + "/health")
    print(res.text)


@click.command()
def test():
    res = requests.get(url=Server.URL + "/test")
    print(res.text)


@click.command()
def subscribe():
    email = input("email: ")
    update_subscribe(email)


@click.command()
def unsubscribe():
    with open(Files.USER_EMAIL, "r") as f:
        email = f.read()
    data = {"email": email}
    requests.post(url=Server.URL + "/unsubscribe", json=data)
    os.remove(Files.USER_EMAIL)
