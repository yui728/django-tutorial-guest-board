FROM django

RUN mkdir -p /opt/apps/django-tutorial-guest-board
WORKDIR /opt/apps/django-tutorial-guest-board

COPY ./src/requirements.txt ./

CMD pip install --upgrade pip && \
  pip install -r requirements.txt && \
  python3 manage.py collectstatic --clear && \
  echo "run gunicorn" && \
  echo gunicorn -v && \
  gunicorn config.wsgi

EXPOSE 8000