FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/vinttem-api

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


RUN pip install --upgrade pip

COPY requirements.txt /usr/src/vinttem-api/
RUN pip install -r requirements.txt

COPY . /usr/src/vinttem-api/

RUN sed -i 's/\r$//g' /usr/src/vinttem-api/entrypoint.sh
RUN chmod +x /usr/src/vinttem-api/entrypoint.sh

ENTRYPOINT ["/usr/src/vinttem-api/entrypoint.sh"]