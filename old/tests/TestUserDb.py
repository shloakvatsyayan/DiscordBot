import unittest
import json


class TestUserDb(unittest.TestCase):
    def test_create_user(self):
        """
        userid    balance       inv
        shloak     10            100
        prateek    20            70
        aarna      30            110
        :return:
        """
        all_users = {}
        user = {'bal': 30, 'inv': 110}
        all_users['arrna'] = user
        user = {'bal': 10, 'inv': 100}
        all_users['shloak'] = user
        user = {'bal': 20, 'inv': 70}
        all_users['prateek'] = user
        with open('userdb.json', 'w') as f:
            json.dump(all_users, f, sort_keys=True, indent=4)

    def test_read_user(self):
        with open('userdb.json' , 'r') as f:
            all_users = json.load(f)
        print(all_users)


if __name__ == '__main__':
    unittest.main()
