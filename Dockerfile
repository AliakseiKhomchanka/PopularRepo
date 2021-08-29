FROM python:alpine3.14

MAINTANER Aliaksei Khomchanka "khomchankaa@gmail.com"

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT [ "flask" ]

CMD [ "run --port=5000" ]