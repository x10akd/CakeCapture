import requests, os, json, environ, uuid, hmac, hashlib, base64

env = environ.Env()
environ.Env.read_env()

LINE_PAY_API_URL = "https://sandbox-api-pay.line.me/v3/payments/request"
LINE_PAY_CHANNEL_ID = env("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = env("LINE_PAY_CHANNEL_SECRET")
CALLBACK_URL = "http://127.0.0.1:8000/orders"


def generate_signature(uri, nonce, payload, secret):
    message = f"{uri}{json.dumps(payload)}{nonce}"
    signature = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode("utf-8")


def request_line_pay(amount, order_id):
    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": LINE_PAY_CHANNEL_ID,
        "X-LINE-ChannelSecret": LINE_PAY_CHANNEL_SECRET,
    }

    packages = {
        "amount": amount,
        "currency": "TWD",
        "orderId": order_id,
        "packages": [
            {
                "id": "package-1",
                "amount": amount,
                "name": "Sample Package",
                "products": [
                    {"name": "Sample Product", "quantity": 1, "price": amount}
                ],
            }
        ],
    }

    redirectUrls = {
        "confirmUrl": CALLBACK_URL + "/confirm",
        "cancelUrl": CALLBACK_URL + "/cancel",
    }

    payload = {
        "amount": amount,
        "currency": "TWD",
        "orderId": order_id,
        "packages": packages["packages"],
        "redirectUrls": redirectUrls,
    }

    nonce = str(uuid.uuid4())
    signature = generate_signature(
        "/v3/payments/request", nonce, payload, LINE_PAY_CHANNEL_SECRET
    )

    headers.update(
        {"X-LINE-Authorization-Nonce": nonce, "X-LINE-Authorization": signature}
    )

    response = requests.post(
        LINE_PAY_API_URL, headers=headers, data=json.dumps(payload)
    )
    print("=" * 10)
    print(LINE_PAY_API_URL)
    print("=" * 10)
    print(response.json())
    print("=" * 10)

    return response.json()
