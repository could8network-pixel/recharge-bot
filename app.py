from flask import Flask, request
import requests
import time

app = Flask(__name__)

# CHANGE THESE
API_TOKEN = "0dba0b41-fa14-4671-9cf7-e1217155218b"
DEVICE_ID = "46083"
MROBOTICS_TOKEN = "a7a5444d-1153-4f86-825c-6a45147d48f6"

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

    print("Sender:", sender)
    print("Message:", message)

    if not sender:
        return "OK"

    # START RECHARGE
    if message.lower() == "recharge":
        users[sender] = {"step": "mobile"}
        send_message(sender, "📱 Mobile number ayakkuka")

    # MOBILE NUMBER
    elif sender in users and users[sender]["step"] == "mobile":
        users[sender]["mobile"] = message
        users[sender]["step"] = "operator"
        send_message(sender, "📡 Operator ayakkuka (JIO/AIRTEL/BSNL/VI)")

    # OPERATOR
    elif sender in users and users[sender]["step"] == "operator":
        users[sender]["operator"] = message.upper()
        users[sender]["step"] = "amount"
        send_message(sender, "💰 Recharge amount ayakkuka")

    # AMOUNT
    elif sender in users and users[sender]["step"] == "amount":
        users[sender]["amount"] = message
        users[sender]["step"] = "confirm"

        send_message(
            sender,
            f"✅ Confirm Recharge\n\n"
            f"Number: {users[sender]['mobile']}\n"
            f"Operator: {users[sender]['operator']}\n"
            f"Amount: ₹{users[sender]['amount']}\n\n"
            f"Reply YES to continue"
        )

    # CONFIRM
    elif sender in users and users[sender]["step"] == "confirm":

        if message.upper() == "YES":

            operator_map = {
                "JIO": 5,
                "AIRTEL": 2,
                "BSNL": 4,
                "VODAFONE": 1,
                "VI": 1,
                "IDEA": 3
            }

            company_id = operator_map.get(
                users[sender]["operator"].upper()
            )

            if not company_id:
                send_message(sender, "❌ Invalid Operator")
                users.pop(sender, None)
                return "OK"

            send_message(sender, "⏳ Recharge Processing...")

            order_id = str(int(time.time()))

            response = requests.post(
                "https://mrobotics.in/api/recharge",
                data={
                    "api_token": MROBOTICS_TOKEN,
                    "mobile_no": users[sender]["mobile"],
                    "amount": users[sender]["amount"],
                    "company_id": company_id,
                    "order_id": order_id,
                    "is_stv": "false"
                }
            )

            result = response.json()

            if result.get("status") == "success":
                send_message(
                    sender,
                    f"✅ Recharge Success\n\n"
                    f"Number: {users[sender]['mobile']}\n"
                    f"Amount: ₹{users[sender]['amount']}"
                )
            else:
                send_message(
                    sender,
                    f"❌ Recharge Failed\n\n"
                    f"{result.get('response', 'Unknown Error')}"
                )

            users.pop(sender, None)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
