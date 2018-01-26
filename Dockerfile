FROM python:3-alpine3.6

RUN apk add --no-cache \
    linux-headers bash gcc musl-dev libjpeg libpng \
    libpq gettext postgresql-dev uwsgi uwsgi-python3

WORKDIR /code
COPY ./ /code/

RUN pip3 install pipenv
RUN pipenv install --system

CMD /code/utils/docker-command.sh
