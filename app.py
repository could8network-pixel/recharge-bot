from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def webhook():
    sender = request.args.get("from")
    message = request.args.get("message")

    print("Sender:", sender)
    print("Message:", message)

    return "Message Received"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
