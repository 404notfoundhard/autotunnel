import requests
import time
import re
import subprocess
from config import ConfigurationObj
from jinja2 import Environment, FileSystemLoader


conf_obj = ConfigurationObj()
loader = FileSystemLoader('template')
env = Environment(loader=loader)
my_template = env.get_template('AutoSSH.service.j2')
ports_find_regex = re.compile(r'([0-9]{5}(?=:localhost:22)'
                              r'|[0-9]{5}(?=:localhost:3306)'
                              r'|[0-9]{5}(?=:localhost:4000))')


def render_autossh_unit(ssh_port_R, db_port_R, vnc_port_R):
    conf_obj.data['R_ssh_port'] = ssh_port_R
    conf_obj.data['R_mysql_port'] = db_port_R
    conf_obj.data['R_vnc_port'] = vnc_port_R

    output_file = my_template.render(data=conf_obj.data)
    with open('/etc/systemd/system/AutoSSH.service', 'w') as file:
        file.write(output_file)
        file.write('\n')


def daemonReload():
    cmd = ['systemctl', 'daemon-reload']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()


def unitCommunicate(action):
    cmd = ['systemctl', action, 'AutoSSH.service']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()


if __name__ == "__main__":
    while True:
        r = requests.post(conf_obj.api_url, data=conf_obj.token)
        try:
            with open('/etc/systemd/system/AutoSSH.service', 'r') as file:
                service_autossh_raw = file.read()
        except FileNotFoundError:
            render_autossh_unit(r.json()['ssh_port'],
                                r.json()['db_port'],
                                r.json()['vnc_port'])
            daemonReload()
            unitCommunicate('enable')
            unitCommunicate('start')

        service_autossh = service_autossh_raw.split('\n')
        for line in service_autossh:
            if re.search('ExecStart', line):
                autossh_ports = re.findall(ports_find_regex, line)
                break

        if (
                (int(autossh_ports[0]) != r.json()['ssh_port'])
                or (int(autossh_ports[1]) != r.json()['db_port'])
                or (int(autossh_ports[2]) != r.json()['vnc_port'])
           ):
            render_autossh_unit(r.json()['ssh_port'],
                                r.json()['db_port'],
                                r.json()['vnc_port'])
            daemonReload()
            unitCommunicate('restart')

        time.sleep(5)
