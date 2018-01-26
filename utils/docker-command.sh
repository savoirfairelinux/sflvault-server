#!/bin/bash

PYTHONUNBUFFERED=1

RUN_UWSGI=0
RUN_STATIC=0
RUN_MIGRATE=1
RUN_NOTHING=0

set -e

cd /code
OPTS=`getopt -o tpn --long test,prod,nomigrate -- "$@"`
[ $? -eq 0 ] || {
    echo "Incorrect options provided"
    exit 1
}
eval set -- "$OPTS"

while true; do
  case "$1" in
    -t | --test)
      RUN_NOTHING=1;
      ;;
    -n | --nomigrate)
      RUN_MIGRATE=0;
      ;;
    -p | --prod)
      RUN_STATIC=1;
      RUN_UWSGI=1;
      ;;
    --)
      break
      ;;
  esac
  shift
done

echo "#------#"

if [ "$RUN_STATIC" == 1 ]; then
  printf "#--- Run collectstatic to collect new assets ---# \n"
  python manage.py collectstatic --noinput > /dev/null
fi

if [ "$RUN_MIGRATE" == 1 ]; then
  printf "#--- Run migrations ---# \n"
  python manage.py migrate > /dev/null
fi

if [ "$RUN_UWSGI" == 1 ]; then
  printf "#--- Run production server ---# \n"
  uwsgi --ini=/code/uwsgi.ini
elif [ "$RUN_NOTHING" == 0 ]; then
  printf "#--- Run development server ---# \n"
  python manage.py runserver 0.0.0.0:8000
fi

exit 0
