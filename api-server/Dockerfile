FROM python:3.6-alpine
WORKDIR /app
COPY . /app

RUN apk update \
    && apk add openssh-server \
    && apk add postgresql-libs gcc musl-dev postgresql-dev  \
    && pip3 install --no-cache-dir -r /app/requirements.txt \
    && adduser -D service_user \
    #set password - 'qwe'
    && user=`cat /etc/shadow | grep service_user` \
    && sed -i '/service_user/d' /etc/shadow  \
    && echo $user | sed 's/!/$6$Kj\/TEArfQSN3mVK8$J1\/\/1gN84GXhvxGp8py.PtyuArf3p59qtC1Xj9R9PL999SoC7NSbAzx5fDDrRMDS\/QJ0UlhepX6KxP1VJi7461/' >> /etc/shadow \
    && mkdir /home/service_user/.ssh \
    && ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N "" \
    && cat /app/key.pub >> /home/service_user/.ssh/authorized_keys

CMD [ "/bin/sh", "/app/docker-entrypoint.sh"]
