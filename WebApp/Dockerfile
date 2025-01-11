FROM python:3.10.8-slim-bullseye

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y pkg-config libmariadb-dev-compat build-essential

RUN mkdir /app
COPY . /app

WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]