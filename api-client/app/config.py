from os import environ, uname


class ConfigurationObj(object):
    __api_host = environ['API_HOST']
    __api_port = environ['API_PORT']
    __local_hostname = uname()[1]
    __path_ssh_key = environ['PATH_SSH_KEY']
    __service_user = environ['SERVICE_USER']
    __remote_host = environ['REMOTE_HOST']

    data = {'R_ssh_port': None,
            'R_mysql_port': None,
            'R_vnc_port': None,
            'path_ssh_key': __path_ssh_key,
            'service_user': __service_user,
            'remote_host': __remote_host}

    api_url = ('http://'
               + __api_host+':'+__api_port
               + '/get_info/'
               + __local_hostname)

    token = {'token': environ['API_TOKEN']}
