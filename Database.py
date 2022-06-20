import json
import os
import config


def _load_json( file_name):
    if not os.path.isfile(file_name):
        return {}
    file_ptr = open(file_name, 'r')
    return json.load(file_ptr)


def _save_json(dict_obj, file_name):
    file_ptr = open(file_name, 'w')
    json.dump(dict_obj, file_ptr)
    file_ptr.close()


class Database:
    file_name_coins = "coins.json"
    file_name_invs = "inv.json"
    file_name_hecked = "hecked.json"

    def __init__(self):
        self.app_config = config.AppConfig()
        self.db_dir = self.app_config.get_config_dir()
        self.coins_file = os.path.join(self.db_dir, Database.file_name_coins)
        self.invs_file = os.path.join(self.db_dir, Database.file_name_invs)
        self.hecked_file = os.path.join(self.db_dir, Database.file_name_hecked)
        self._load_db()

    def _load_db(self):
        self.coins = _load_json(self.coins_file)
        self.inv = _load_json(self.invs_file)
        self.hecked = _load_json(self.hecked_file)

    def _save_db(self):
        _save_json(self.coins, self.coins_file)
        _save_json(self.inv, self.invs_file)
        _save_json(self.hecked, self.hecked_file)

    def add_money(self, uid, amt):
        if uid in self.coins:
            user_amt = self.coins[uid]
            self.coins[uid] = user_amt + amt
        else:
            self.coins[uid] = amt
            self.inv[uid] = 0
        self._save_db()

    def add_inv(self, uid, amt):
        if uid in self.inv:
            user_amt = self.inv[uid]
            self.inv[uid] = user_amt + amt
        self._save_db()

