from os import environ


class Configuration(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ('postgres+psycopg2://'
                               + environ['POSTGRES_LOGIN'] + ':'
                               + environ['POSTGRES_PASSWORD'] + '@'
                               + environ['POSTGRES_ADDRESS'] + ':'
                               + environ['POSTGERS_PORT'] + '/'
                               + environ['POSTGRES_DATABASE'])

    SECRET_KEY = environ['SECRET_KEY'].encode('utf-8')
    render_host = environ['HOST_FOR_SSH_CONNECT']
    render_service_user = environ['SERVICE_USER']
