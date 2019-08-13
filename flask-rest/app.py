from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Configuration
import psycopg2
# import os
from datetime import datetime
# from OpenSSL import SSL

context = ('/home/notfound/python_4_learn/flask-rest/certs/rest.crt',
           '/home/notfound/python_4_learn/flask-rest/certs/rest.key')


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
    date_time = db.Column(db.String)

    def __init__(self):
        hostname = self.hostname
        ssh_port = self.ssh_port
        db_port = self.db_port
        vnc_port = self.vnc_port
        server = self.server
        date_time = self.date_time

    def __repr__(self):
        return '< %r>' % self.hostname


class ConnectlistSchema(ma.Schema):
    class Meta:
        fields = ('hostname', 'ssh_port', 'db_port', 'vnc_port',
                  'server', 'date_time')


# Init schema
connect_list = ConnectlistSchema(strict=True)
# connect_lists = ConnectlistSchema(strict=True, many=True)


@app.errorhandler(404)
def notfound(nfd):
    exit(0)


@app.route('/get_info/<hostname>', methods=['GET'])
def get_ports_info(hostname):
    ports_info = Connectlist.query.filter_by(hostname=hostname).first()
    if ports_info is None:
        exit(0)
    ports_info.date_time = str(datetime.utcnow())
    db.session.commit()
    return connect_list.jsonify(ports_info)


if __name__ == "__main__":
    app.run()
