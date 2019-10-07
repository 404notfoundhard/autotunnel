# autotunnel
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)  
Complex for creating and monitoring ssh tunnels

#### For what?
I have several dozen server behind NAT.  
And im tired manually setup port for ssh tunnel for this servers.  
Where i should store ports for reverse connection and monitor the condition of the tunnels?  

#### functional in web-server:

![](https://user-images.githubusercontent.com/9219437/66038990-d0c75180-e53d-11e9-838e-9872ec252efc.png)
* copy ssh command to clipboard
* show info about port binding
* remove host from binding
* status remote host(red - down, green - up)

\#############  
***api-server*** used same database !!!  
\#############


#### function in api-client:
* create systemd [ AutoSSH service](api-client/app/template/AutoSSH.service.j2)
* check port changing
* report connection status  


#### example:
You can up test environmnet  
with vagrant:
```
cd infra/test_environmnet && vagrant up && cd ../ansible && ansible-playbook -i inventory.yml addservice.yml
```
or use docker =)
```
cd infra/ && docker-compose up -d --build
```

#### Install:
Use [ansible playbook](infra/ansible/)  
But first configure [ansible vars](infra/ansible/vars.yml)
#### TL;DR

### overview
#### web-server:


It can be placed anything, but ***api-server*** used same database.  
served by gunicorn


###### environment for web-server:
```yml
POSTGRES_LOGIN=login"         #--|
POSTGRES_PASSWORD=password"   #  |
POSTGRES_ADDRESS=127.0.0.1"   #   ----4 connect 2 db
POSTGERS_PORT=5432"           #  |
POSTGRES_DATABASE=database"   # --
SECRET_KEY=secret_CSRF"       # ---- CSRF token
HOST_FOR_SSH_CONNECT=sub.example.loc"   # ---- used for render template
SERVICE_USER=service_user"              # ---- used for render template
```


#### api-server:
the api-server must be located where the ssh tunnel is established  

example:
```bash
|                     |<---SSH tunnel--->|                 |
|server with public ip|<----request------|Server behind nat|
|     api-server      |-----response---->|                 |
```
What in *request*?
Its a simple http request with post method 
```bash
curl http://192.168.99.100:9999/get_info/hostname_server_behind_nat -d "token=12345_secret"
```
What in *responce*?
```json
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
```yml
POSTGRES_LOGIN=login"         #--|
POSTGRES_PASSWORD=password"   #  |
POSTGRES_ADDRESS=127.0.0.1"   #   ----4 connect 2 db
POSTGERS_PORT=5432"           #  |
POSTGRES_DATABASE=database"   # --
SECRET_TOKEN=secret_token_for_api_auth_in_api # ---- Auth token for api-client
HOST_FOR_SSH_CONNECT=remotehost.loc # ---- temporary env
```


#### api-client
Generates a unit file and monitors changes on the server. If the ports for some reason will be changed in the database, it will form a new unit file and restart autossh service
###### environment for api-client:
```yml
API_PROTO=http # ---- if not defined it uses http by default, change to https if ou use reverse proxy with ssl
API_HOST=10.1.1.1 
API_PORT=9999
API_TOKEN=secret_token_for_auth_in_api           # ---- token for auth to api-server
PATH_SSH_KEY=/path/to/key/for/ssh/tunnel         # ---- ssh tunnel key
SERVICE_USER=user_who_accept_ssh_reverse_connect # ---- remote user for ssh tunnel 
HOST_FOR_SSH_CONNECT=remotehost.loc              # ---- host for ssh tunnel
REVERSE_PROXY_PATH # if not defined it null by default
```
