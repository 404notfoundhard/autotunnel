# autotunnel
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)  
Complex for creating and monitoring ssh tunnels

#### For what?
I have several dozen server behind NAT.  
And im tired manually setup port for ssh tunnel for this servers.  
Where i should store ports for reverse connection and monitor the condition of the tunnels?  
I decided to write this small project

#### Install:
web:
1) Install postgresql
2) Create database
3) Move web-server folder to /srv/
4) Install python 3.6, python3.6-venv 
5) Create virtual-environment in web-server folder  
6) Install python requirements to virtual env
4) set environmnet and path in [web-server/hermes.service](web-server/hermes.service)
5) reload systemctl and start service

or use ansible playbook [install web-server](infra/example-ansible-playbook) :)

#### TL;DR

### overview
#### web-server:
![](https://user-images.githubusercontent.com/9219437/66038990-d0c75180-e53d-11e9-838e-9872ec252efc.png)

It can be placed anything, but ***api-server*** used same database.  
served by gunicorn


###### environment for web-server:
```
POSTGRES_LOGIN=postgres
POSTGRES_PASSWORD=root  
POSTGRES_ADDRESS=127.0.0.1
POSTGERS_PORT=5436
POSTGRES_DATABASE=my_bd
SECRET_KEY=awesome-secret-key-12345_anti_CSRF
HOST_FOR_SSH_CONNECT=remotehost.loc
SERVICE_USER=user_who_accept_ssh_reverse_connect
```



#### api-server:
the api-server must be located where the ssh tunnel is established  

example:
```
|                     |<---SSH tunnel--->|                 |
|server with public ip|<----request------|Server behind nat|
|     api-server      |-----response---->|                 |
```
What in *request*?
Its a simple http request with post method 
```
curl http://192.168.99.100:9999/get_info/hostname_server_behind_nat -d "token=12345_secret"
```
What in *responce*?
```
{ "db_port":48013,
  "hostname":"hostname_server_behind_nat",
  "last_connect_time":"2019-10-02 11:33:57.712741",
  "server":"remotehost.loc",
  "ssh_port":48012,
  "vnc_port":48014
}
```
as we can see this is a json that the api client will process and create a unit file and start the service with autossh
###### environment for api-server:
```
POSTGRES_LOGIN=postgres
POSTGRES_PASSWORD=root
POSTGRES_DATABASE=my_bd
POSTGRES_ADDRESS=127.0.0.1
POSTGERS_PORT=5436
SECRET_TOKEN=secret_token_for_api_auth_in_api
HOST_FOR_SSH_CONNECT=remotehost.loc
```

#### api-client
Generates a unit file and monitors changes on the server. If the ports for some reason will be changed in the database, it will form a new unit file and restart autossh service
###### environment for api-client:
```
API_PROTO=http # if not defined it uses https by default
API_HOST=10.1.1.1
API_PORT=9999
API_TOKEN=secret_token_for_auth_in_api
PATH_SSH_KEY=/path/to/key/for/ssh/tunnel
SERVICE_USER=user_who_accept_ssh_reverse_connect
HOST_FOR_SSH_CONNECT=remotehost.loc
REVERSE_PROXY_PATH # if not defined it null by default
```
