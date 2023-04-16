FROM python:3.10.5-alpine

WORKDIR /code

COPY requirements.txt /code
COPY . /code

EXPOSE 5000:5000
EXPOSE 5432:5432

RUN apk update 
RUN apk add py3-psycopg2
RUN apk add postgresql-dev
RUN apk add --no-cache postgresql
RUN apk add gcc
RUN apk add python3-dev
RUN apk add musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
CMD ["flask", "--app", "FlaskApp", "run"]
