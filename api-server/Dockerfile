# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.6-alpine
WORKDIR /app
COPY . /app

RUN --mount=id=apk,type=cache,target=/var/cache/apk,sharing=locked \
    --mount=id=apk,type=cache,target=/var/lib/apk/,sharing=locked \
    --mount=id=apk,type=cache,target=/etc/apk/cache/,sharing=locked apk update && apk add openssh-server postgresql-libs gcc musl-dev postgresql-dev

RUN --mount=id=pip3,type=cache,target=/opt/pip3_cache,sharing=locked  pip3 install --cache-dir /opt/pip3_cache -r /app/requirements.txt

RUN adduser -D service_user \
    #set password - 'qwe'
    && user=`cat /etc/shadow | grep service_user` \
    && sed -i '/service_user/d' /etc/shadow  \
    && echo $user | sed 's/!/$6$Kj\/TEArfQSN3mVK8$J1\/\/1gN84GXhvxGp8py.PtyuArf3p59qtC1Xj9R9PL999SoC7NSbAzx5fDDrRMDS\/QJ0UlhepX6KxP1VJi7461/' >> /etc/shadow \
    && mkdir /home/service_user/.ssh \
    # create ssh daemon key
    && ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N "" \ 
    && cat /app/key.pub >> /home/service_user/.ssh/authorized_keys

CMD [ "/bin/sh", "/app/docker-entrypoint.sh"]
