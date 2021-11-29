DOCKER_IMAGE:=server

build:
	docker build --tag ${DOCKER_IMAGE} .

test:
	docker run --rm ${DOCKER_IMAGE}
run:
	docker run --rm -it --publish 8000:8000 ${DOCKER_IMAGE}