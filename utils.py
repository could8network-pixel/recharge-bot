import json
import os

WALLET_FILE = "wallet.json"
HISTORY_FILE = "history.json"
USERS_FILE = "users.json"


def load_json(file_name, default):
    if not os.path.exists(file_name):
        return default

    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


def get_wallet():
    return load_json(WALLET_FILE, {})


def save_wallet(wallet):
    save_json(WALLET_FILE, wallet)


def get_history():
    return load_json(HISTORY_FILE, [])


def save_history(history):
    save_json(HISTORY_FILE, history)


def get_users():
    return load_json(USERS_FILE, {})


def save_users(users):
    save_json(USERS_FILE, users)


def wallet_balance(number):
    wallet = get_wallet()
    return wallet.get(number, 0)


def add_wallet(number, amount):

    wallet = get_wallet()

    wallet[number] = wallet.get(number, 0) + amount

    save_wallet(wallet)

    return wallet[number]


def deduct_wallet(number, amount):

    wallet = get_wallet()

    if wallet.get(number, 0) < amount:
        return False

    wallet[number] -= amount

    save_wallet(wallet)

    return True


def add_history(data):

    history = get_history()

    history.append(data)

    save_history(history)
