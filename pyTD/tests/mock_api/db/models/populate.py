# Populate all tables

from datetime import datetime, timedelta

from db.engine import session

from db.models.account import Account
from db.models.auth import Client, Token

import random


client = {
    "client_id": "TEST11@AMER.OAUTHAP",
    "redirect_uri": "https://127.0.0.1:8080",
}

account = {
    "accountId": random.randint(100000000, 999999999),
    "currentBalances": {
        "accruedInterest": 333.333,
        "bondValue": 444.00
    },
    "client_id": "TEST11@AMER.OAUTHAP"
}


def add_client():
    new_client = Client(**client)
    access_token, refresh_token = Token.generate_tokens()
    access_expires = datetime.now() + timedelta(minutes=90)
    refresh_expires = datetime.now() + timedelta(days=300)
    new_tokens = Token(client_id=new_client.client_id,
                       access_token=access_token, refresh_token=refresh_token,
                       access_expires=access_expires,
                       refresh_expires=refresh_expires)
    session.add(new_client)
    session.add(new_tokens)
    session.commit()
    return new_client


def add_account():
    new_account = Account(accountId=account["accountId"],
                          client_id="TEST11@AMER.OAUTHAP")
    session.add(new_account)
    session.commit()
    return new_account


def add_all():
    add_client()
    add_account()
