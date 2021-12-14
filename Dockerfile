FROM python:alpine3.9

RUN mkdir /app
WORKDIR /app

ADD app.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0" ]