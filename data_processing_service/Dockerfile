FROM python:3.12-slim-bookworm

RUN apt-get -y update

RUN apt-get -y install git

WORKDIR /app

COPY ./requirements_consumers.txt .

RUN pip install --no-cache-dir -r requirements_consumers.txt

COPY . .

CMD python3 ./main.py;
