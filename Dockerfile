FROM django

RUN ["mkdir", "/usr/bin/app/django-tutorial"]
WORKDIR /usr/bin/myapps/django-tutorial

RUN pip install pipenv -y
RUN pipenv install -y

CMD pipenv update

CMD python3 manage.py collectstatic

CMD gunicorn config.wsgi

EXPOSE 8000