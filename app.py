from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "WhatsBot Webhook Running"

@app.route("/", methods=["POST"])
def webhook():
    print("Received:", request.form)
    return "OK"
