IMAGE_NAME=upathway-robot-facade
IMAGE_TAG=0.0.0
DOCKERFILE=docker/Dockerfile

.PHONY: build build-no-cache up down reset logs logs-f

build:
	docker build --tag $(IMAGE_NAME):$(IMAGE_TAG) -f $(DOCKERFILE) .

build-no-cache:
	docker build --tag $(IMAGE_NAME):$(IMAGE_TAG) --no-cache -f $(DOCKERFILE) .

up:
	docker compose up -d

down:
	docker compose down 

reset:
	docker compose restart

logs:
	docker compose logs

logs-f:
	docker compose logs -f
