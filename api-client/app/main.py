import requests
import time
import os
import re
import subprocess
from jinja2 import Environment, FileSystemLoader


loader = FileSystemLoader('template')
env = Environment(loader=loader)
my_template = env.get_template('AutoSSH.service.j2')
hostname = os.uname()[1]
token = {'token': '12345'}
ports_find_regex = re.compile(r'([0-9]{5}(?=:localhost:22)|[0-9]{5}(?=:localhost:3306)|[0-9]{5}(?=:localhost:4000))')
# temaplate
data = {'R_ssh_port': None, 'R_mysql_port': None, 'R_vnc_port': None}


def recreate_autossh_unit(ssh_port_R, db_port_R, vnc_port_R):
    data['R_ssh_port'] = ssh_port_R
    data['R_mysql_port'] = db_port_R
    data['R_vnc_port'] = vnc_port_R
    output_file = my_template.render(data=data)
    with open('/etc/systemd/system/AutoSSH.service', 'w') as file:
        file.write(output_file)
        file.write('\n')


def daemonReload():
    cmd = ['systemctl', 'daemon-reload']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print('Stdout: %s\nStderr: %s' % stdout, stderr)


def unitCommunicate(action):
    cmd = ['systemctl', action, 'AutoSSH.service']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print('Stdout: %s\nStderr: %s' % stdout, stderr)


if __name__ == "__main__":
    while True:
        r = requests.post('http://10.10.10.1:9999/get_info/'+hostname, data=token)
        try:
            with open('test_output.txt', 'r') as file:
                service_autossh_raw = file.read()
        except:
            recreate_autossh_unit(r.json()['ssh_port'], r.json()['db_port'], r.json()['vnc_port'])
            daemonReload()
            unitCommunicate('enable')
            unitCommunicate('start')

        service_autossh = service_autossh_raw.split('\n')
        for line in service_autossh:
            if re.search('ExecStart', line):
                autossh_ports = re.findall(ports_find_regex, line)
                break

        if (autossh_ports[0] != r.json()['ssh_port']) and (autossh_ports[1] != r.json()['db_port']) and (autossh_ports[2] != r.json()['vnc_port']):
            recreate_autossh_unit(r.json()['ssh_port'], r.json()['db_port'], r.json()['vnc_port'])
            daemonReload()
            unitCommunicate('restart')

        time.sleep(5)
