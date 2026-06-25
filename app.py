
from flask import Flask, request
import requests

app = Flask(__name__)

# CHANGE THESE
API_TOKEN = "0dba0b41-fa14-4671-9cf7-e1217155218b"
DEVICE_ID = "46083"

users = {}

def send_message(mobile, text):
    try:
        r = requests.get(
            "https://whatsbot.tech/api/send_sms",
            params={
                "api_token": API_TOKEN,
                "mobile": mobile,
                "message": text,
                "device_id": DEVICE_ID
            }
        )

        print("========== WHATSBOT DEBUG ==========")
        print("TO:", mobile)
        print("MESSAGE:", text)
        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)
        print("===================================")

    except Exception as e:
        print("SEND MESSAGE ERROR:", str(e))


@app.route("/", methods=["GET", "POST"])
def webhook():

    sender = request.args.get("from")
    message = request.args.get("message", "").strip()

    print("========== INCOMING ==========")
    print("SENDER:", sender)
    print("MESSAGE:", message)
    print("==============================")

    if not sender:
        return "OK"

    if message.lower() == "recharge":
        users[sender] = {"step": "mobile"}
        send_message(sender, "📱 Mobile number ayakkuka")

    elif sender in users and users[sender]["step"] == "mobile":
        users[sender]["mobile"] = message
        users[sender]["step"] = "operator"
        send_message(sender, "📡 Operator ayakkuka (JIO/AIRTEL/BSNL/VI)")

    elif sender in users and users[sender]["step"] == "operator":
        users[sender]["operator"] = message.upper()
        users[sender]["step"] = "amount"
        send_message(sender, "💰 Recharge amount ayakkuka")

    elif sender in users and users[sender]["step"] == "amount":

        users[sender]["amount"] = message
        users[sender]["step"] = "confirm"

        send_message(
            sender,
            f"✅ Confirm\n\n"
            f"Number: {users[sender]['mobile']}\n"
            f"Operator: {users[sender]['operator']}\n"
            f"Amount: ₹{users[sender]['amount']}\n\n"
            f"Reply YES"
        )

    elif sender in users and users[sender]["step"] == "confirm":

        if message.upper() == "YES":
            send_message(sender, "⏳ Recharge processing...")
            send_message(sender, "✅ Recharge Request Received")

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
