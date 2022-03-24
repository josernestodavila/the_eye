FROM python:3.10.2-slim-buster
WORKDIR /var/task
RUN apt clean && apt update && apt install gcc libpq-dev procps -y

COPY requirements requirements
RUN pip install -r requirements/development.txt

COPY . /var/task
