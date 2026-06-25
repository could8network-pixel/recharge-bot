from flask import Flask, request, jsonify
import requests
import os
import uuid

app = Flask(__name__)

API_TOKEN = os.getenv("a7a5444d-1153-4f86-825c-6a45147d48f6")

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "MRobotics Recharge API"
    })

@app.route("/recharge", methods=["POST"])
def recharge():

    try:
        data = request.get_json()

        mobile = data["mobile"]
        amount = data["amount"]
        operator = data["operator"]

        company_map = {
            "VI": 1,
            "AIRTEL": 2,
            "IDEA": 3,
            "BSNL": 4,
            "JIO": 5,
            "DISHTV": 6,
            "TATASKY": 7
        }

        company_id = company_map.get(operator.upper())

        if not company_id:
            return jsonify({
                "status": "error",
                "message": "Invalid Operator"
            })

        order_id = str(uuid.uuid4().int)[:10]

        payload = {
            "api_token": API_TOKEN,
            "mobile_no": mobile,
            "amount": amount,
            "company_id": company_id,
            "order_id": order_id,
            "is_stv": "false"
        }

        response = requests.post(
            "https://mrobotics.in/api/recharge",
            data=payload,
            timeout=60
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/balance")
def balance():

    try:

        response = requests.post(
            "https://mrobotics.in/api/operator_balance",
            params={
                "api_token": API_TOKEN
            }
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "error": True,
            "message": str(e)
        })


@app.route("/status/<order_id>")
def status(order_id):

    try:

        response = requests.post(
            "https://mrobotics.in/api/order_id_status",
            params={
                "api_token": API_TOKEN,
                "order_id": order_id
            }
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "error": True,
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
