class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:root@192.168.99.100:5432/my_bd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = "localhost:9999"
