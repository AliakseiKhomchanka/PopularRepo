FROM python:alpine3.14

MAINTAINER Aliaksei Khomchanka "khomchankaa@gmail.com"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT [ "python" ]

HEALTHCHECK CMD curl --fail http://localhost:5000/service/live || exit 1

CMD [ "app.py" ]
