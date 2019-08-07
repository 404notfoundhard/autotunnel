# from OpenSSL import SSL

# context = SSL.Context(SSL.TLSv1_2_METHOD)
# context.use_privatekey_file('rest.key')
# context.use_certificate_file('cert_bundle.crt')


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:root@192.168.99.100:5432/my_bd'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    Threaded = True
    SERVER_NAME="localhost:9999"
    # ssl_context = (context)
