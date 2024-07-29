FROM python:3.12-slim-bookworm

RUN apt-get -y update

RUN apt-get -y install git

WORKDIR /app

COPY ./requirements_producers.txt .

RUN pip install --no-cache-dir -r requirements_producers.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--app", "app", "--port", "8000"]
