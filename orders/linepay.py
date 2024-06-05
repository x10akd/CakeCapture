import requests
import os
import json
import environ

env = environ.Env()
environ.Env.read_env()

LINE_PAY_API_URL = "https://api-pay.line.me/v2/payments/request"
LINE_PAY_CHANNEL_ID = env("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = env("LINE_PAY_CHANNEL_SECRET")
CALLBACK_URL = "http://127.0.0.1:8000/orders"


def request_line_pay(amount, order_id):
    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": LINE_PAY_CHANNEL_ID,
        "X-LINE-ChannelSecret": LINE_PAY_CHANNEL_SECRET,
    }
    payload = {
        "amount": amount,
        "currency": "TWD",
        "orderId": order_id,
        "redirectUrls": {
            "confirmUrl": CALLBACK_URL + "/confirm",
            "cancelUrl": CALLBACK_URL + "/cancel",
        },
    }

    response = requests.post(
        LINE_PAY_API_URL, headers=headers, data=json.dumps(payload)
    )
    return response.json()
