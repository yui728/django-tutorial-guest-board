FROM python:3.7

RUN apt-get update \
    && apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
	postgresql-client \
	nginx \
	&& rm -rf /var/lib/apt/lists/* \
	&& systemctl enable nginx.service

WORKDIR /usr/src/app
COPY ./src/requirements.txt .
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=config.production

CMD python3 manage.py collectstatic --clear && \
  echo "run gunicorn" && \
  echo "gunicorn -v:"  && \
  gunicorn -v && \
  gunicorn config.wsgi -b 0.0.0.0:8000

EXPOSE 8000