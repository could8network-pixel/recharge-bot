from flask import Flask, request
import requests
import json
import os
import time

from config import (
    WHATSBOT_API_TOKEN,
    DEVICE_ID,
    MYSTAREC_TOKEN,
    ADMIN_NUMBER,
    OPERATORS
)

app = Flask(__name__)

WALLET_FILE = "wallet.json"
HISTORY_FILE = "history.json"

users = {}


def load_wallet():
    if not os.path.exists(WALLET_FILE):
        return {}
    with open(WALLET_FILE, "r") as f:
        return json.load(f)


def save_wallet(data):
    with open(WALLET_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def send_message(mobile, message):

    r = requests.get(
        "https://whatsbot.tech/api/send_sms",
        params={
            "api_token": WHATSBOT_API_TOKEN,
            "mobile": mobile,
            "message": message,
            "device_id": DEVICE_ID
        }
    )

    print("SEND STATUS:", r.status_code)
    print("SEND RESPONSE:", r.text)


@app.route("/", methods=["GET", "POST"])
def webhook():

    sender = request.args.get("from")
    message = request.args.get("message", "").strip()

    print("FROM:", sender)
    print("MESSAGE:", message)

    if not sender:
        return "OK"

    wallets = load_wallet()
    history = load_history()

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

