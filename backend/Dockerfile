FROM python:3.10-alpine

WORKDIR app
COPY . .

#COPY ../requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]


