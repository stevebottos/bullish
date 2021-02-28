import click

from bullish import __version__, commands


@click.version_option(__version__)
@click.group()
def bullish():
    pass


@bullish.group(name="news")
def news_tree():
    pass


@bullish.group(name="watchlist")
def watchlist_tree():
    pass

news_tree.add_command(commands.fetch)

watchlist_tree.add_command(commands.ls)
watchlist_tree.add_command(commands.add)