import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
import pickle
import time

from fastapi import FastAPI, BackgroundTasks
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

from server.data.secrets import Email
from server.scraper import get_email_content

app = FastAPI()

if not os.path.exists("data/subscribers.json"):
    with open("data/subscribers.json", "w+") as f:
        json.dump({}, f)

if not os.path.exists("data/todays_entries.pkl"):
    with open("data/todays_entries.pkl", "wb+") as f:
        pickle.dump([], f)


class Subscription(BaseModel):
    email: str
    watchlist: list = []


@app.on_event("startup")
@repeat_every(seconds=60 * 10)  # 10 minutes
async def alerts_process():

    with open("data/subscribers.json") as f:
        subscriber_data = json.load(f)

        if not len(subscriber_data):
            return

        message = MIMEMultipart()
        message["From"] = Email.USER
        message["Subject"] = "TEST"
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        session.starttls()
        session.login(Email.USER, Email.PASS)
        for email, tickers in subscriber_data.items():
            print(f"Sending mail to {email}")
            message["To"] = email
            try:
                email_formatted = await get_email_content(tickers)
                session.sendmail(Email.USER, email, email_formatted)
            except Exception as e:
                print(e)

        session.quit()
        print("Mail sent")


@app.get("/health")
async def health():
    return 200


@app.post("/update_subscribe")
async def subscribe(request: Subscription):
    email = request.email
    watchlist = request.watchlist

    with open("data/subscribers.json", "r+") as f:
        data = json.load(f)
        data[email] = watchlist

        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return {"message": "Successfully subscribed."}


@app.post("/unsubscribe")
async def unsubscribe(request: Subscription):
    email = request.email

    with open("data/subscribers.json", "r+") as f:
        data = json.load(f)

        if email in data:
            del data[email]
        else:
            return {"message": "Email not found in subscriptions list"}

        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return {"message": "Successfully unsubscribed."}
