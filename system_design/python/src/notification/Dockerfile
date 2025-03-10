FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update\
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip --no-cache-dir


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

CMD [ "python3", "consumer.py" ]