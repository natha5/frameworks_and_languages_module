_DOCKER_COMPOSE:=USER=$(shell id -u):$(shell id -g) docker-compose
DOCKER_COMPOSE:=${_DOCKER_COMPOSE} --file docker-compose.yml
DOCKER_COMPOSE_EXAMPLE:=${DOCKER_COMPOSE} --file docker-compose.example.server.yml --file docker-compose.example.client.yml
DOCKER_COMPOSE_TEST:=${DOCKER_COMPOSE} --file docker-compose.cypress.yml --file docker-compose.test.yml
DOCKER_COMPOSE_EXAMPLE_TEST:=${DOCKER_COMPOSE_EXAMPLE} --file docker-compose.cypress.yml --file docker-compose.test.yml

.PHONY: help
.DEFAULT_GOAL:=help
help:	## display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2 } END{print ""}' $(MAKEFILE_LIST)
	# deafult server port 8000
	# default client port 8001

run:  ##
	${DOCKER_COMPOSE} up
run_example:  ## run example server and client containers
	${DOCKER_COMPOSE_EXAMPLE} up
run_example_server:  ##
	${DOCKER_COMPOSE} --file docker-compose.example.server.yml up --build server
		## run --rm server /bin/sh
#run_example_client:  ##
#	${DOCKER_COMPOSE} --file docker-compose.example.client.yml up

#test:  ##
#	${DOCKER_COMPOSE_TEST} up --build
#	${DOCKER_COMPOSE_TEST} down
test_server:  ##
	${DOCKER_COMPOSE_TEST} up --build server_test
	${DOCKER_COMPOSE_TEST} down
test_client:  ##
	${DOCKER_COMPOSE_TEST} up --build client_test
	${DOCKER_COMPOSE_TEST} down

#test_example:  ##
#	${DOCKER_COMPOSE_EXAMPLE_TEST} up
#	${DOCKER_COMPOSE_EXAMPLE_TEST} down
test_example_server:  ##
	${DOCKER_COMPOSE_EXAMPLE_TEST} up --build server_test
	${DOCKER_COMPOSE_EXAMPLE_TEST} down
test_example_client:  ##
	${DOCKER_COMPOSE_EXAMPLE_TEST} up --build client_test
	${DOCKER_COMPOSE_EXAMPLE_TEST} down

cypress:  ## Launch local cypress from container (requires an XServer and DISPLAY env)
	${DOCKER_COMPOSE_EXAMPLE_TEST} run --rm --env DISPLAY client_test open --project .
	${DOCKER_COMPOSE_EXAMPLE_TEST} down
cypress_cmd:
	${_DOCKER_COMPOSE} --file docker-compose.cypress.yml \
		run --rm client_test \
			${CYPRESS_CMD}
