FROM python:3.6-slim
WORKDIR /app
COPY . /app

EXPOSE 8081

RUN pip3 install --no-cache-dir -r /app/requirements.txt

CMD [ "gunicorn",  \
      "--chdir", "/app/app/", \
      "--access-logfile", "-", \
      "--error-logfile", "-" , \
      "--bind", "0.0.0.0:8081", "main:app"]
