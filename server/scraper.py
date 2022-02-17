import os
import requests
import json
from datetime import datetime
import pickle
import re

USERS = ["Newsfilter", "fla", "cctranscripts"]

MONTHS = {
    1: ["January", "Jan"],
    2: ["February", "Feb"],
    3: ["March"],
    4: ["April"],
    5: ["May"],
    6: ["June"],
    7: ["July"],
    8: ["August", "Aug"],
    9: ["September", "Sep"],
    10: ["October", "Oct"],
    11: ["November", "Nov"],
    12: ["December", "Dec"],
}


async def scrape(users_of_interest, tickers_of_interest):

    scraped_messages = []
    url_str = "https://api.stocktwits.com/api/2/streams/user/{}.json"

    for user in users_of_interest:
        url = url_str.format(user)
        response = requests.request("GET", url)

        parsed = json.loads(response.text)
        messages = parsed["messages"]

        for message in messages:
            message_body = message["body"]
            for ticker in tickers_of_interest:
                search_key = "".join(("$", ticker, " "))
                if search_key in message_body:
                    scraped_messages.append(message_body)
    return scraped_messages


async def format_email_message(email_content):
    return "\n---\n".join(email_content)


async def save_list_as_pickle(lst, fname="data/todays_entries.pkl"):
    with open(os.path.join(fname), "wb+") as f:
        pickle.dump(lst, f)


async def load_list_from_pickle(fname="data/todays_entries.pkl"):
    with open(os.path.join(fname), "rb") as f:
        return pickle.load(f)


async def get_email_content(tickers_of_interest):
    today = datetime.now()
    if today.time().hour == 6 and today.time().minute <= 10:
        todays_entries = load_list_from_pickle()

        info_dict = {}
        info_dict["tickers"] = []
        info_dict["message"] = []

        for entry in todays_entries:

            tickers = re.findall(r"[$][A-Za-z]+", entry)

            for ticker in tickers:
                info_dict["tickers"].append(ticker)
                info_dict["message"].append(entry)

        # headlines = pd.DataFrame.from_dict(info_dict)

        # # To filter out the bullshit
        # headlines = headlines.loc[~headlines["message"].str.contains("Why")]
        # headlines = headlines.loc[~headlines["message"].str.contains("Stocks Moving")]
        # headlines = headlines.loc[~headlines["message"].str.contains("gainers")]
        # headlines = headlines.loc[~headlines["message"].str.contains("Gainers")]
        # headlines = headlines.loc[~headlines["message"].str.contains("movers")]
        # headlines = headlines.loc[~headlines["message"].str.contains("Movers")]
        # headlines = headlines.loc[~headlines["message"].str.contains("Trading Higher")]
        # headlines = headlines.loc[~headlines["message"].str.contains("Market Update")]

        # headlines.to_csv(
        #     os.path.join("data", "records", str(today).split(" ")[0] + ".csv")
        # )

        todays_entries = []
        save_list_as_pickle(todays_entries)

    todays_entries = await load_list_from_pickle()
    email_raw = await scrape(USERS, tickers_of_interest)
    email_raw_filtered = [email for email in email_raw if email not in todays_entries]

    if len(email_raw_filtered):
        todays_entries = email_raw_filtered + todays_entries
        await save_list_as_pickle(todays_entries)

        # Only send an email if it contains one of the special tickers we're watching
        email_messages = []
        for ticker in tickers_of_interest:
            for entry in email_raw_filtered:
                search_key = "".join(("$", ticker, " "))
                if search_key in entry:
                    email_messages.append(entry)

        if len(email_messages) > 0:
            email_formatted = await format_email_message(email_messages)

            return email_formatted
        return None
