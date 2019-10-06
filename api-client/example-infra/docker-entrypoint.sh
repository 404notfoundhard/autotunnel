#!/bin/bash

#
# a simplified example of work api-client
# because systemd cannot be used in docker
#

while true; do
   curl "$API_PROTO://$API_HOST:$API_PORT/get_info/`cat /etc/hostname`" -d "token=$API_TOKEN" > ports.txt
   sleep 5
   SSH_PORT=`cat ports.txt | grep -Po '(?<=ssh_port"\:)[0-9]{5}'`
   DB_PORT=`cat ports.txt | grep -Po '(?<=db_port"\:)[0-9]{5}'`
   VNC_PORT=`cat ports.txt | grep -Po '(?<=vnc_port"\:)[0-9]{5}'`

   ps auxf | grep 'autossh.*localhost' | grep -v grep &> /dev/null
   comp_val=$?

   if [[ $comp_val == 0 ]]; then # if exit code is '0' ?
      continue
   fi

   autossh -f -N -R $SSH_PORT:localhost:22 -R $DB_PORT:localhost:3306 -R $VNC_PORT:localhost:4000 $SERVICE_USER@$HOST_FOR_SSH_CONNECT -i /apicli/example-infra/key
done
