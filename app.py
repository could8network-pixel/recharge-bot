from flask import Flask, request
import requests

app = Flask(__name__)

API_TOKEN = "0dba0b41-fa14-4671-9cf7-e1217155218b"
DEVICE_ID = "46083"

@app.route("/", methods=["GET", "POST"])
def webhook():
    sender = request.args.get("from")
    message = request.args.get("message")

    if message and message.lower() == "recharge":
        requests.get(
            "https://whatsbot.tech/api/send_sms",
            params={
                "api_token": API_TOKEN,
                "mobile": sender,
                "message": "📱 Mobile number ayakkuka",
                "device_id": DEVICE_ID
            }
        )

    return "OK"
