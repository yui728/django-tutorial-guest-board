FROM django

RUN mkdir -p /opt/apps/django-tutorial-guest-board
WORKDIR /opt/apps/django-tutorial-guest-board

COPY ./src/requirements.txt ./

CMD pip install --upgrade pip

CMD pip install -r requirements.txt

CMD python3 manage.py collectstatic --clear

CMD ["echo", "run gunicorn"]

CMD ["echo", "gunicorn", "-v"]

CMD ["gunicorn", "config.wsgi"]

EXPOSE 8000