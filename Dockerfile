FROM python:3.10-5alpine

WORKDIR /code

COPY requirements.txt /code
COPY . /code

RUN apt-get update
RUN apt-get install python3.10.5
RUN pip install -r requirements.txt

CMD ["flask", "--app", "FlaskApp", "run"]