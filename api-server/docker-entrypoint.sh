#!/bin/bash

nohup /usr/sbin/sshd -D & 
gunicorn --chdir /app/app/ --access-logfile - --error-logfile - --bind 0.0.0.0:9999 main:app
