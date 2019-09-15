import requests
import time

token = {'token': '12345'}

while True:
    r = requests.post('http://localhost:9999/get_info/test', data=token)
    print(r.json()['ssh_port'], r.json()['db_port'], r.json()['vnc_port'])
    time.sleep(5)
