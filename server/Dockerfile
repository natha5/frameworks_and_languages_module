FROM python:slim

WORKDIR /app/

RUN pip install falcon gunicorn

COPY . .

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0", "app:app" ]


