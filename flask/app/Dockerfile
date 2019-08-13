FROM python:3.6-alpine3.9
COPY ../app /app
RUN pipe install -r requirements.txt
EXPOSE 5000
CMD python3.6 /app/main.py

