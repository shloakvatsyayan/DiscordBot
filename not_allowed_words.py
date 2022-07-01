import requests
import json
import config

cfg = config.AppConfig()
token = cfg.get_oterulu_api_key()
headers = {'x-api-key': token, 'Content-type': 'application/json'}


def check_message(message, threshold=1):
    data = {'text': message}
    data_str = json.dumps(data)
    resp = requests.post(url='https://classify.oterlu.com/v1/text', headers=headers, data=data_str)
    print("Status code:{}".format(resp.status_code))
    r = resp.json()
    return r['labels']
