from flask import Flask, request
import requests

app = Flask(__name__)

API_TOKEN = "0dba0b41-fa14-4671-9cf7-e1217155218b"
DEVICE_ID = "46083"

users = {}

def send_message(mobile, text):
    requests.get(
        "https://whatsbot.tech/api/send_sms",
        params={
            "api_token": API_TOKEN,
            "mobile": mobile,
            "message": text,
            "device_id": DEVICE_ID
        }
    )

@app.route("/", methods=["GET", "POST"])
def webhook():
    sender = request.args.get("from")
    message = request.args.get("message", "").strip()

    if message.lower() == "recharge":
        users[sender] = {"step": "mobile"}
        send_message(sender, "📱 Mobile number ayakkuka")

    elif sender in users and users[sender]["step"] == "mobile":
        users[sender]["mobile"] = message
        users[sender]["step"] = "operator"
        send_message(sender, "📡 Operator ayakkuka (JIO/AIRTEL/BSNL)")

    elif sender in users and users[sender]["step"] == "operator":
        users[sender]["operator"] = message.upper()
        users[sender]["step"] = "amount"
        send_message(sender, "💰 Recharge amount ayakkuka")

    elif sender in users and users[sender]["step"] == "amount":
        users[sender]["amount"] = message

        send_message(
            sender,
            f"✅ Confirm\n\nNumber: {users[sender]['mobile']}\nOperator: {users[sender]['operator']}\nAmount: ₹{message}\n\nReply YES"
        )

        users[sender]["step"] = "confirm"

    elif sender in users and users[sender]["step"] == "confirm":
        if message.upper() == "YES":
            send_message(sender, "⏳ Recharge processing...")
            # MRobotics API ivide add cheyyam
            send_message(sender, "✅ Recharge Request Received")

    return "OK"
