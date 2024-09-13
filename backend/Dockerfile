FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py migrate

ENTRYPOINT [ "uwsgi", "uwsgi.ini" ]