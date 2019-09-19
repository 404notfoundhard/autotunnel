from os import environ, uname


class ConfigurationObj(object):
    __api_host = environ['API_HOST']
    __api_port = environ['API_PORT']
    __api_token = environ['API_TOKEN']
    __local_hostname = uname()[1]

    api_url = ('http://'
               + __api_host+':'+__api_port
               + '/get_info/'
               + __local_hostname)

    token = {'token': __api_token}
