FROM python:3.10.5-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app /code/app
WORKDIR /code/app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
