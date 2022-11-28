FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/vinttem-api

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/vinttem-api/
RUN pip install -r requirements.txt

COPY . /usr/src/vinttem-api/

