import requests
import time
from jinja2 import Environment, FileSystemLoader
import os

loader = FileSystemLoader('template')
env = Environment(loader=loader)
my_template = env.get_template('AutoSSH.service.j2')
# R_ssh_port
# R_mysql_port
# R_vnc_port
hostname = os.uname()[1]

token = {'token': '12345'}

# while True:
r = requests.post('http://localhost:9999/get_info/'+hostname, data=token)
print(r.json()['ssh_port'], r.json()['db_port'], r.json()['vnc_port'])
# time.sleep(5)

data = {'R_ssh_port': r.json()['ssh_port'],
        'R_mysql_port': r.json()['db_port'],
        'R_vnc_port': r.json()['vnc_port']}

loader = FileSystemLoader('template')
env = Environment(loader=loader)
my_template = env.get_template('AutoSSH.service.j2')
output_file = my_template.render(data=data)

with open('test_output.txt', 'w') as file:
    file.write(output_file)
