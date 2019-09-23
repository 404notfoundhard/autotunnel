from os import environ, uname


class ConfigurationObj(object):
    __api_host = environ['API_HOST']
    __api_port = environ['API_PORT']
    __local_hostname = uname()[1]
    __path_ssh_key = environ['PATH_SSH_KEY']
    __service_user = environ['SERVICE_USER']
    __remote_host = environ['HOST_FOR_SSH_CONNECT']
    try:
        __http_proto = environ['API_PROTO']
    except KeyError:
        __http_proto = 'https'
    try:
        __path_for_reverse_proxy = environ['REVERSE_PROXY_PATH']
    except KeyError:
        __path_for_reverse_proxy = ''
    data = {'R_ssh_port': None,
            'R_mysql_port': None,
            'R_vnc_port': None,
            'path_ssh_key': __path_ssh_key,
            'service_user': __service_user,
            'remote_host': __remote_host}

    api_url = (__http_proto
               + '://'
               + __api_host+':'+__api_port
               + __path_for_reverse_proxy
               + '/get_info/'
               + __local_hostname)

    token = {'token': environ['API_TOKEN']}
