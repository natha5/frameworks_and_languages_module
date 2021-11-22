DOCKER_IMAGE:=server_example

run_local:
	python3 main.py

test_local:
	pytest

build:
	docker build --tag ${DOCKER_IMAGE} .

test:
	# DOCKER_BUILDKIT=0 - This runs all the tests on build as part of a multistage build layer
	docker build --tag ${DOCKER_IMAGE} --target test .

run:
	docker run -it --rm --publish 8000:8000 ${DOCKER_IMAGE}
