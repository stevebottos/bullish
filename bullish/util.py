import logging 

from bs4 import BeautifulSoup
import requests


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def trim_down_to_n_dates(dates_and_headlines: dict, n=3):
    delete_keys = list(dates_and_headlines.keys())[n:]
    for k in delete_keys:
        del dates_and_headlines[k]

    return dates_and_headlines


def finviz_scrape(ticker="TSLA"):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    finviz_url = f"https://finviz.com/quote.ashx?t={ticker}"
    response = requests.get(finviz_url, headers=headers)

    if response.status_code != 200: 
        LOGGER.error(f"Problem! {finviz_url} can't be reached")
        return

    page_source = response.text
    soup = BeautifulSoup(page_source, "lxml")

    news_entries = soup.find(id="news-table").find_all("tr")

  
    dates_and_headlines = {}
    current_news_date = None
    for entry in news_entries:
        date_tag = entry.find("td")
        
        if "style" in date_tag.attrs:
            current_news_date = date_tag.text.split(" ")[0]
            dates_and_headlines[current_news_date] = []

        a_tag = entry.find("a")
        dates_and_headlines[current_news_date].append((a_tag.text, a_tag["href"]))

    return dates_and_headlines
    





    
