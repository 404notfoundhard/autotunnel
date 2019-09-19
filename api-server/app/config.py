from os import environ



class Configuration(object):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = ('postgres+psycopg2://'
                               + environ['POSTGRES_LOGIN'] + ':'
                               + environ['POSTGRES_PASSWORD'] + '@'
                               + environ['POSTGRES_ADDRESS'] + ':'
                               + environ['POSTGERS_PORT'] + '/'
                               + environ['POSTGRES_DATABASE'])
    secret_token = environ['SECRET_TOKEN']
    # SERVER_NAME = "10.10.10.1:9999"
