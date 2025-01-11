FROM python:3.10.8-slim-bullseye

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y protobuf-compiler

RUN mkdir /app
COPY . /app

WORKDIR /app

ENV GRPC_RUN_PORT=50051
EXPOSE 50051

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","grpc_rental_server.py"]