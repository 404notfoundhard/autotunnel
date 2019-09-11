class Configuration(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:root@192.168.99.100:5432/my_bd'
    SECRET_KEY = b'?om(quV\q]E:}7gh|@kJ/XzAfs@crdKHp"|dqTFU'
