FROM python:3.6-alpine3.9
COPY app /app
RUN apk add libpq-dev -y && pip3 install -r /app/requirements.txt
EXPOSE 5000
CMD python3.6 /app/main.py

