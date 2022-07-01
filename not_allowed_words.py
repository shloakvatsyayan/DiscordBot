import requests
import json
import config

cfg = config.AppConfig()
token = cfg.get_oterulu_api_key()
headers = {'x-api-key': token, 'Content-type': 'application/json'}

def check_message(message):
    data = {'text': message}
    data_str = json.dumps(data)
    resp = requests.post(url='https://classify.oterlu.com/v1/text', headers=headers, data=data_str)
    resp.status_code
    r = resp.json()
    lables = r['labels']
    return lables

a=check_message("Hi")
if 