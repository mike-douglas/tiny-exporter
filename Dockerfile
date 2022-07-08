FROM python:alpine3.9

RUN mkdir /app
WORKDIR /app

ADD . .

RUN pip install -r requirements.txt && \
    pip install waitress && \
    pip install .

ENTRYPOINT [ "waitress-serve", "--port=5000", "--call", "api:create_app" ]