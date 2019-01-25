#! /usr/bin/env python

"""
Utility script to return cached refresh token if one exists given current
environment configuration

Attempts to find configuration file in configuration directory (located in
either the value of TD_CONFIG_DIR or the default ~/.tdm). Raises an exception
if a refresh token cannot be found or is not valid (expired or malformed)
"""
import datetime
import json
import os
import time

CONFIG_DIR = os.getenv("TD_CONFIG_DIR") or os.path.expanduser("~/.tdm")

CONSUMER_KEY = os.getenv("TD_CONSUMER_KEY")
# Must have consumer key to locate DiskCache file
if CONSUMER_KEY is None:
    raise ValueError("Environment variable TD_CONSUMER_KEY must be set")

CONFIG_PATH = os.path.join(CONFIG_DIR, CONSUMER_KEY)

try:
    with open(CONFIG_PATH, 'r') as f:
        json_data = json.load(f)
        refresh_token = json_data["refresh_token"]
        token = refresh_token["token"]
        now = datetime.datetime.now()
        now = int(time.mktime(now.timetuple()))
        access = int(refresh_token["access_time"])
        expires = int(refresh_token["expires_in"])
        expiry = access + expires
        if expiry > now:
            print(token)
        else:
            raise Exception("Refresh token expired")
except Exception:
    raise Exception("Refresh token could not be retrieved")
