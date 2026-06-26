import requests
import time

from config import (
    WHATSBOT_API_TOKEN,
    DEVICE_ID,
    MYSTAREC_TOKEN
)


def send_message(mobile, message):

    try:

        r = requests.get(
            "https://whatsbot.tech/api/send_sms",
            params={
                "api_token": WHATSBOT_API_TOKEN,
                "mobile": mobile,
                "message": message,
                "device_id": DEVICE_ID
            },
            timeout=30
        )

        print("SEND:", r.text)

        return True

    except Exception as e:
        print("SEND ERROR:", e)
        return False


def recharge(number, amount, spkey, customer_mobile):

    agentid = str(int(time.time()))

    try:

        r = requests.get(
            "https://mystarec.com/api/",
            params={
                "token": MYSTAREC_TOKEN,
                "format": "json",
                "type": "transaction",
                "agentid": agentid,
                "spkey": spkey,
                "number": number,
                "amount": amount,
                "cust_mobile": customer_mobile
            },
            timeout=60
        )

        data = r.json()

        print(data)

        return data

    except Exception as e:

        return {
            "response_code": "ERR",
            "response_msg": str(e)
        }


def check_status(agentid):

    r = requests.get(
        "https://mystarec.com/api/",
        params={
            "token": MYSTAREC_TOKEN,
            "format": "json",
            "type": "check",
            "agentid": agentid
        }
    )

    return r.json()


def balance():

    r = requests.get(
        "https://mystarec.com/api/",
        params={
            "token": MYSTAREC_TOKEN,
            "format": "json",
            "type": "balance"
        }
    )

    return r.json()
