FROM python:alpine

WORKDIR /client/

EXPOSE 8001

COPY . .

CMD ["python3", "-m", "http.server", "8001"]