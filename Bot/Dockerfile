FROM python:3.10-bullseye

WORKDIR /app/bot/

COPY ./ /app/bot/

WORKDIR /tmp/bot/

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip -q install torch
RUN pip -q install transformers
RUN pip install -U "py-cord[voice]"
RUN pip -q install psutil
RUN pip -q install uwuipy
RUN pip -q install unidecode

WORKDIR /app/bot/
