FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

ENV http_proxy=http://rb-proxy-de.bosch.com:8080
ENV https_proxy=http://rb-proxy-de.bosch.com:8080

RUN pip install -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]