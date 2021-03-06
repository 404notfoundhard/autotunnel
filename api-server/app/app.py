from flask import Flask, request, jsonify
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2
import subprocess
# import os
from datetime import datetime
# from OpenSSL import SSL


app = Flask(__name__)

# Import configuration from config.py
app.config.from_object(Configuration)
# Init db
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Connectlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(254), unique=True)
    ssh_port = db.Column(db.Integer, unique=True)
    db_port = db.Column(db.Integer, unique=True)
    vnc_port = db.Column(db.Integer, unique=True)
    server = db.Column(db.String(15))
    last_connect_time = db.Column(db.String)

    def __init__(self, hostname, ssh_port, db_port,
                 vnc_port, server, last_connect_time):
        self.hostname = hostname
        self.ssh_port = ssh_port
        self.db_port = db_port
        self.vnc_port = vnc_port
        self.server = server
        self.last_connect_time = last_connect_time

    def __repr__(self, hostname, ssh_port, db_port,
                 vnc_port, server, last_connect_time):
        return '< %r>' % self.hostname


class ConnectlistSchema(ma.Schema):
    class Meta:
        fields = ('hostname', 'ssh_port', 'db_port', 'vnc_port',
                  'server', 'last_connect_time')


# Init schema
connect_list = ConnectlistSchema(strict=True)


def kill_socket(hostname):
    current_pid = None
    ssh_port = Connectlist.query.with_entities(Connectlist.ssh_port)
    filtred_port = ssh_port.filter_by(hostname=hostname).first()
    cmd = ['sudo', 'ss', '-tlnp']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    # get current freezing reverse ssh pid
    for i in stdout.decode('utf-8').split('\n'):
        if '127.0.0.1:'+str(filtred_port[0]) in i:
            """
            fast search pid, without regexp
            example string:
            LISTEN 0 128 127.0.0.1:48004 0.0.0.0:* users:(("sshd",pid=10826,fd=14))
            """
            current_pid = i.split('pid=')[1].split(',')[0]
    if current_pid is None:
        return 'ok'
    for connect_string in stdout.decode('utf-8').split('\n'):
        if 'pid='+current_pid in connect_string:
            bad_socket = connect_string.split()[3]
            if '127.0.0.1' in bad_socket:
                port_4_kill = bad_socket.split(':')[1]
                socket_kill = ['sudo', 'ss', '--kill', 'state', 'listening', 'src', ':'+port_4_kill]
                proc = subprocess.Popen(socket_kill, stdout=subprocess.PIPE)
                proc.communicate()
    return 'ok'


def find_available_ports():
    # get busy ports from linux
    with open('/proc/net/tcp', 'r') as f:
        connect_lines = f.readlines()
    busy_ports_tcpv = []
    for line in connect_lines[1:]:
        local_hex_socket = line.split()[1].split(':')
        if '0100007F' == local_hex_socket[0]:
            busy_ports_tcpv.append(int('0x'+local_hex_socket[1], 16))
    busy_ports_tcpv = set(busy_ports_tcpv)
    # get busy ports from db
    busy_ports_from_db_raw = Connectlist.query.with_entities(
                                                        Connectlist.ssh_port,
                                                        Connectlist.db_port,
                                                        Connectlist.vnc_port
                                                        ).all()
    busy_ports_from_db = []
    # because ORM return data like this:
    # "[(12345, 12346, 12347), (48000, 48002, 48001)]"
    for i in busy_ports_from_db_raw:
        for x in i:
            busy_ports_from_db.append(x)

    busy_ports_from_db = set(busy_ports_from_db)
    busy_ports_tcpv.update(busy_ports_from_db)

    reserved_ports = {i for i in range(48000, 51001)}
    available_ports = list(reserved_ports - busy_ports_tcpv)
    available_ports.sort()
    ssh_port = available_ports[0]
    db_port = available_ports[1]
    vnc_port = available_ports[2]

    return ssh_port, vnc_port, db_port


def add_new_host(hostname):
    ssh_port, vnc_port, db_port = find_available_ports()
    new_usr = Connectlist(hostname=hostname,
                          ssh_port=ssh_port,
                          db_port=db_port,
                          vnc_port=vnc_port,
                          server=Configuration.remote_host,
                          last_connect_time=str(datetime.utcnow()))
    new_usr.hostname = hostname
    db.session.add(new_usr)
    db.session.commit()
    db.session.flush()
