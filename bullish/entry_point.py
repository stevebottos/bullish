import click

from bullish import __version__, news, watchlist, notes, alerts


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


@bullish.group(name="notes")
def notes_tree():
    pass


@bullish.group(name="alerts")
def alerts_tree():
    pass

news_tree.add_command(news.fetch)
news_tree.add_command(news.report)

watchlist_tree.add_command(watchlist.ls)
watchlist_tree.add_command(watchlist.add)
watchlist_tree.add_command(watchlist.remove)

notes_tree.add_command(notes.ls)
notes_tree.add_command(notes.update)

alerts_tree.add_command(alerts.start)
alerts_tree.add_command(alerts.stop)
alerts_tree.add_command(alerts.check)