Server

Running server in container:
```bash
cd server
make build
make run
```
ctrl + c to exit


Running locally:
```bash
cd server
make run_local
```
ctrl + c to exit

Server is built using Falcon framework. Uses Gunicorn and httpd for container and local servers respectively.

Server
======