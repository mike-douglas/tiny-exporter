FROM python:alpine3.9

RUN mkdir /app
WORKDIR /app

ADD . .

RUN pip install -r requirements.txt
RUN pip install .

ENV FLASK_APP=api

ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0" ]