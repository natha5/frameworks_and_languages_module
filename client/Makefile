DOCKER_IMAGE:=client

build:
	docker build --tag ${DOCKER_IMAGE} .

test:
	docker run --rm ${DOCKER_IMAGE}

run:
	docker run --rm --publish 8001:8001 ${DOCKER_IMAGE}

