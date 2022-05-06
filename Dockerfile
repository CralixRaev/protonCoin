FROM python:latest
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]