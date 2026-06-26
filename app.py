from flask import Flask, request
from api import send_message, recharge
from config import OPERATORS

app = Flask(__name__)
users = {}

@app.route("/", methods=["GET","POST"])
def webhook():
    sender = request.args.get("from")
    message = (request.args.get("message") or "").strip()

    if not sender:
        return "OK"

    if message.lower() == "recharge":
        users[sender] = {"step":"mobile"}
        send_message(sender,"📱 Enter mobile number")

    elif sender in users and users[sender]["step"]=="mobile":
        users[sender]["mobile"]=message
        users[sender]["step"]="operator"
        send_message(sender,"📡 Operator: JIO / VI / IDEA / BSNL STV / BSNL TOPUP")

    elif sender in users and users[sender]["step"]=="operator":
        op = message.upper()
        if op not in OPERATORS:
            send_message(sender,"❌ Invalid operator")
            return "OK"
        users[sender]["operator"]=op
        users[sender]["step"]="amount"
        send_message(sender,"💰 Enter recharge amount")

    elif sender in users and users[sender]["step"]=="amount":
        users[sender]["amount"]=message
        users[sender]["step"]="confirm"
        send_message(
            sender,
            f"Confirm Recharge\n\n"
            f"Number: {users[sender]['mobile']}\n"
            f"Operator: {users[sender]['operator']}\n"
            f"Amount: ₹{users[sender]['amount']}\n\n"
            f"Reply YES"
        )

    elif sender in users and users[sender]["step"]=="confirm":
        if message.upper()=="YES":
            result = recharge(
                users[sender]["mobile"],
                users[sender]["amount"],
                OPERATORS[users[sender]["operator"]],
                sender
            )
            code = result.get("response_code")
            if code=="TXN":
                send_message(sender,"✅ Recharge Successful")
            elif code=="TUP":
                send_message(sender,"⏳ Recharge Pending")
            else:
                send_message(sender,f"❌ Failed: {result.get('response_msg','Unknown error')}")
            users.pop(sender,None)
        else:
            send_message(sender,"❌ Cancelled")
            users.pop(sender,None)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
