DOCKER_IMAGE:=server


run_local:
	#python3 -m http.server 8000
	python3 app.py

test_local:
	pytest


build:
	docker build --tag ${DOCKER_IMAGE} .

test:
	docker run --rm ${DOCKER_IMAGE}
run:
	docker run --rm -it --publish 8000:8000 ${DOCKER_IMAGE}