# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.6-slim
WORKDIR /app
COPY . /app

EXPOSE 8081

RUN --mount=id=pip3,type=cache,target=/opt/pip3_cahce,sharing=locked \
    pip3 install --cache-dir /opt/pip3_cahce -r /app/requirements.txt

CMD [ "gunicorn",  \
      "--chdir", "/app/app/", \
      "--access-logfile", "-", \
      "--error-logfile", "-" , \
      "--bind", "0.0.0.0:8081", "main:app"]
