FROM python:3.7

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./src/requirements.txt .
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

CMD python3 manage.py collectstatic --clear && \
  echo "run gunicorn" && \
  echo "gunicorn -v:"  && \
  gunicorn -v && \
  gunicorn config.wsgi -b 0.0.0.0:8000

EXPOSE 8000