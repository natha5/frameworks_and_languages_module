Client
======
Running client in container:
```bash
cd client
make build
make run
```
ctrl + c to exit


Running locally:
```bash
cd client
make run_local
```
ctrl + c to exit

Testing client:
Either
```bash
cd root
make client_test
```

Client is built using Vue.js framework.
Included files:
* __init.py__
* Dockerfile
* Makefile
* index.html
* README.md
* package.json
* package-lock.json

References:

* Stylesheet taken from: https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/css/bootstrap.min.css
* JS data fetching adapted from: https://www.geeksforgeeks.org/javascript-fetch-method/
