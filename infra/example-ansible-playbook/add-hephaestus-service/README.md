Add hephaestus service
=========

Simple role for add unit file for systemd  
Copy api-client source files and run service


Role Variables
--------------

##### api_host:  ip adderss or FQDN for api-server  
##### api_port:  for api server
##### api_token:  
api service use simple authoriztion in post method.  
You should set token in zeus.service(api-server)  
##### reverse_proxy_path:  
If you use reverse proxy(nginx, apache or something else)  
set path to api-server in this param  
##### host_for_ssh_connect:  
ip address for make ssh tunnel  
##### ssh_key_path: 
param for autossh, needed for established ssh tunnel in main server  
auth only by key
##### service_user: 
remote user for ssh tunnel


Example Playbook
----------------

All role variables define in "defaults"


---
```
- name: add api-client
  hosts: ssh-cli
  become: yes    ### this directive is mandatory
  roles:
  - add-hephaestus-service
```
License
-------

BSD

