FROM python:3.9

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app/backend
RUN pip install -r /app/requirements.txt

EXPOSE 8000
