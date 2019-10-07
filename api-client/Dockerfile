# syntax=docker/dockerfile:1.0.0-experimental
FROM alpine:latest

WORKDIR /apicli
COPY . /apicli


RUN --mount=id=apk,type=cache,target=/var/cache/apk,sharing=locked \
    --mount=id=apk,type=cache,target=/var/lib/apk/,sharing=locked \
    --mount=id=apk,type=cache,target=/etc/apk/cache/,sharing=locked apk update \
&& apk add openssh-client curl autossh

CMD [ "/bin/sh","/apicli/docker-entrypoint.sh" ]
