import click
import requests 

from server.constants import Server

@click.command()
def test():
    res = requests.get(url=Server.URL + "/")
    print(res)
