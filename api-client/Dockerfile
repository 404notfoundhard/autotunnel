FROM alpine:latest

WORKDIR /apicli
COPY . /apicli

RUN apk update \
    && apk add openssh-client curl autossh

CMD [ "/bin/sh","/apicli/example-infra/docker-entrypoint.sh" ]
