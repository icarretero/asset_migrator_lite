SHELL:=/bin/bash
#Include here your remote repo
REMOTE_REPOSITORY:=local

IMAGE_NAME:=asset_migrator_lite
IMAGE_TAG:=0.1.1

build:
	docker build --rm \
	-t $(REMOTE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG) \
	-f Dockerfile \
	.

push:
	docker push $(REMOTE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG)

run:
	docker run \
	--env-file .env.local \
	$(REMOTE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG)

run-local:
	docker run \
	--env-file .env.local \
	--add-host=host.docker.internal:host-gateway \
	-e MYSQL_HOST=host.docker.internal \
	$(REMOTE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: build push run run-local
