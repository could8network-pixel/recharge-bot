from flask import Flask, request
from api import send_message
from utils import (
    get_users,
    save_users
)
from config import OPERATORS

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def webhook():

    sender = request.args.get("from")
    message = request.args.get("message", "").strip()

    print("==========================")
    print("FROM :", sender)
    print("MESSAGE :", message)
    print("==========================")

    if not sender:
        return "OK"

    users = get_users()

    # Start Recharge
    if message.lower() == "recharge":

        users[sender] = {
            "step": "mobile"
        }

        save_users(users)

        send_message(
            sender,
            "📱 Enter Mobile Number"
        )

        return "OK"

    # Mobile
    if sender in users and users[sender]["step"] == "mobile":

        users[sender]["mobile"] = message
        users[sender]["step"] = "operator"

        save_users(users)

        send_message(
            sender,
            "Select Operator\n\n"
            "1. JIO\n"
            "2. VI\n"
            "3. IDEA\n"
            "4. BSNL STV\n"
            "5. BSNL TOPUP"
        )

        return "OK"

    # Operator
    if sender in users and users[sender]["step"] == "operator":

        operator_map = {
            "1": "JIO",
            "2": "VI",
            "3": "IDEA",
            "4": "BSNL STV",
            "5": "BSNL TOPUP"
        }

        if message not in operator_map:

            send_message(
                sender,
                "Invalid Operator."
            )

            return "OK"

        users[sender]["operator"] = operator_map[message]
        users[sender]["step"] = "amount"

        save_users(users)

        send_message(
            sender,
            "💰 Enter Recharge Amount"
        )

        return "OK"

    # Amount
    if sender in users and users[sender]["step"] == "amount":

        users[sender]["amount"] = message
        users[sender]["step"] = "confirm"

        save_users(users)

        send_message(
            sender,
            f"""Confirm Recharge

Mobile : {users[sender]['mobile']}

Operator : {users[sender]['operator']}

Amount : ₹{users[sender]['amount']}

Reply YES"""
        )

        return "OK"
       # Confirm Recharge
    if sender in users and users[sender]["step"] == "confirm":

        if message.upper() == "YES":

            send_message(sender, "⏳ Processing Recharge...")

            spkey = OPERATORS.get(users[sender]["operator"])

            from api import recharge

            result = recharge(
                number=users[sender]["mobile"],
                amount=users[sender]["amount"],
                spkey=spkey,
                customer_mobile=sender
            )

            print(result)

            code = result.get("response_code")

            if code == "TXN":

                send_message(
                    sender,
                    f"""✅ Recharge Successful

Mobile : {users[sender]['mobile']}

Amount : ₹{users[sender]['amount']}

Txn ID : {result.get('txn_id')}"""
                )

            elif code == "TUP":

                send_message(
                    sender,
                    f"""⏳ Recharge Pending

Txn ID : {result.get('txn_id')}

Please wait."""
                )

            else:

                send_message(
                    sender,
                    f"""❌ Recharge Failed

{result.get('response_msg')}"""
                )

            users.pop(sender, None)

            save_users(users)

            return "OK"

        else:

            send_message(sender, "Reply YES to continue.")

            return "OK" 

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
