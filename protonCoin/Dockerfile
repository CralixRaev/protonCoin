FROM python:3.12-alpine

RUN adduser -D protonCoin

WORKDIR /home/protonCoin

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY . .
RUN chmod +x boot.sh

ENV FLASK_APP .

USER protonCoin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
