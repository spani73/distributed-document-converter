FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update\
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential && apt-get install -y git\
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip --no-cache-dir


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

RUN git clone https://github.com/mailjet/mailjet-apiv3-python && \
    cd mailjet-apiv3-python && \
    pip install .

COPY . /app

CMD [ "python3", "consumer.py" ]