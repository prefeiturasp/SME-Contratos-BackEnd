FROM python:3.6.15-bullseye

ADD . /code
WORKDIR /code

RUN python -m pip --no-cache install -U pip && \
    python  -m pip --no-cache install -r requirements/production.txt

EXPOSE 8000
