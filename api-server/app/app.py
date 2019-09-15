from flask import Flask, request, jsonify
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2
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


def find_available_ports():
    # get busy ports from linux
    connect_lines = open("/proc/net/tcp").readlines()
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
    vnc_port = available_ports[1]
    db_port = available_ports[2]

    return ssh_port, vnc_port, db_port


def add_new_host(hostname):
    ssh_port, vnc_port, db_port = find_available_ports()
    print('##########################')
    print(ssh_port, vnc_port, db_port)
    print('##########################')
    new_usr = Connectlist(hostname=hostname,
                          ssh_port=ssh_port,
                          db_port=db_port,
                          vnc_port=vnc_port,
                          server='monit.tru.io',
                          last_connect_time=str(datetime.utcnow())
                          )
    new_usr.hostname = hostname
    db.session.add(new_usr)
    db.session.commit()
    db.session.flush()
