import requests
import time
import re
import os
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


def customLogger(txt4w):
    with open('/var/log/yaica/api-cli.log', 'a') as api_log:
        api_log.write(txt4w)


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


def autosshCommunicate(action):
    cmd = ['systemctl', action, 'AutoSSH.service']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    # customLogger(str(stderr))
    # customLogger(str(stdout))


if __name__ == "__main__":
    time_out_retry_connect = 0
    reconnection_flag = False
    if not os.path.exists('/var/log/yaica/'):
        os.makedirs('/var/log/yaica/')

    while True:
        while True:
            try:
                conf_obj.token['reconnect_status'] = reconnection_flag
                r = requests.post(conf_obj.api_url, data=conf_obj.token, timeout=4)
                # try json decode
                # test = r.json()['ssh_port']
                # del test
            except Exception as request_conn_err:
                time_out_retry_connect += 5
                customLogger('[ERROR] Connection failed at [%s]: ' % time.ctime())
                customLogger(str(request_conn_err)+'\n')
                customLogger('Next connection after: '
                             + str(time_out_retry_connect))
                customLogger('\n--------------------------\n')

                time.sleep(time_out_retry_connect)

                if reconnection_flag is False:
                    customLogger('Stoping AutoSSH service....\n')
                    autosshCommunicate('stop')
                reconnection_flag = True

            else:
                # wait when api-server close socket
                # prevent "socket alredy used"
                if reconnection_flag is True:
                    customLogger('[INFO] Connection restored at [%s]' % time.ctime())
                    customLogger('\n--------------------------\n')
                    conf_obj.token['reconnect_status'] = reconnection_flag
                    time.sleep(5)
                    customLogger('Starting AutoSSH service....')
                    autosshCommunicate('start')
                    reconnection_flag = False
                time_out_retry_connect = 0
                break
        try:
            with open('/etc/systemd/system/AutoSSH.service', 'r') as file:
                service_autossh_raw = file.read()
        except FileNotFoundError:
            render_autossh_unit(r.json()['ssh_port'],
                                r.json()['db_port'],
                                r.json()['vnc_port'])
            daemonReload()
            autosshCommunicate('enable')
            autosshCommunicate('start')
        except Exception as my_error:
            customLogger('[ERROR] Start failed at [%s]: ' % time.ctime())
            customLogger(str(my_error)+'\n')
            render_autossh_unit(r.json()['ssh_port'],
                                r.json()['db_port'],
                                r.json()['vnc_port'])
            daemonReload()
            autosshCommunicate('enable')
            autosshCommunicate('start')
            
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
            autosshCommunicate('restart')

        time.sleep(5)
