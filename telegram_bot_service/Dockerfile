FROM python:3.9-slim-bookworm

RUN apt-get -y update

RUN apt-get -y install git

WORKDIR /app

COPY ./requirements_bot.txt .

RUN pip install --no-cache-dir -r requirements_bot.txt

COPY . .

CMD python3 ./main.py;
