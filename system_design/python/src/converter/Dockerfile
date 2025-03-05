FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    libgl1\
    libgl1-mesa-glx \ 
    libglib2.0-0 -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip --no-cache-dir

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

CMD [ "python3", "consumer.py" ]