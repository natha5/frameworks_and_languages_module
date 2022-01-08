Server
======
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

Testing server:
Either
```bash
cd root
make server_test
```
or
```bash
cd server
make build
make run
```
then, in another terminal:
```bash
cd server_test
pip install pytest
pytest test_api.py
```

Server is built using Falcon framework. Uses Gunicorn and httpd for container and local servers respectively.

Included files:
* __init.py__
* dataStore.py
* Dockerfile
* Makefile
* app.py
* README.md

References:

*dataStore.py adapted from Allan's example.
*CORS handling adapted from https://github.com/falconry/falcon/issues/1220
