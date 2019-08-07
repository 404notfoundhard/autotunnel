from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
ma = Marshmallow(app)


def time_on_status(time_from_db):
    if time_from_db is None:
        return 'danger'
    time_limit = timedelta(0, 300)
    ctime = datetime.utcnow()
    db_time = datetime.strptime(time_from_db, '%Y-%m-%d %H:%M:%S.%f')
    if time_limit < (ctime - db_time):
        return 'danger'
    else:
        return 'success'

class Connectlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(254), unique=True)
    ssh_port = db.Column(db.Integer, unique=True)
    db_port = db.Column(db.Integer, unique=True)
    vnc_port = db.Column(db.Integer, unique=True)
    server = db.Column(db.String(15))
    date_time = db.Column(db.String)

    def __init__(self):
        id = self.id
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
        fields = ('id', 'hostname', 'ssh_port', 'db_port', 'vnc_port',
                  'server', 'date_time')
