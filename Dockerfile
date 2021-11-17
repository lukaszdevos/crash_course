FROM python:3.9

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app/backend
RUN pip install -r /app/requirements.txt
ENV DJANGO_SETTINGS_MODULE crashcourse.settings
