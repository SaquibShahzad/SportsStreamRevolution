# Just for running python file, no rabbitmq
FROM python:3.8

WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y netcat
RUN pip install --no-cache-dir pika
COPY . .
CMD ["sleep", "infinity"]