import json
import os
import time as t
import threading

coins = {}
inv = {}

file_name_coins = "coins.json"
file_name_inv = "inv.json"



def load_coins():
    if not os.path.isfile(file_name_coins):
        return {}
    file_ptr = open(file_name_coins, 'r')
    return json.load(file_ptr)

def load_inv():
    if not os.path.isfile(file_name_inv):
        return {}
    file_ptr = open(file_name_inv, 'r')
    return json.load(file_ptr)

def save_coins():
    file_ptr = open(file_name_coins, 'w')
    json.dump(coins, file_ptr)
    file_ptr.close()

def save_inv():
    file_ptr = open(file_name_inv, 'w')
    json.dump(inv, file_ptr)
    file_ptr.close()


def add_money(uid, amt):
    if uid in coins:
        user_amt = coins[uid]
        coins[uid] = user_amt + amt
    else:
        coins[uid] = amt
        inv[uid] = 0
    save_coins()

def add_inv(uid, amt):
    if uid in inv:
        user_amt = inv[uid]
        inv[uid] = user_amt + amt
    save_inv()

def set_inv(uid, amt):
    if uid in inv:
        inv[uid]=amt
    save_inv()

def get_money(uid):
    if uid in coins:
        return coins[uid]
    else:
        return None

def get_inv(uid):
    if uid in inv:
        return inv[uid]
    else:
        return None

def start_inv_thread():
    t = threading.Thread(target=add_inv_loop)
    t.start()

def add_inv_loop():
    while True:
        for i in inv:
            add_inv(i, 1)
        t.sleep(1)

def is_user_registered(uid):
    if uid in coins:
        return True
    else:
        return False

coins = load_coins()
inv = load_inv()