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
	-e MYSQL_HOST=$(MYSQL_HOST) \
	-e MYSQL_PWD=$(MYSQL_PWD) \
	-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
	-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
	$(REMOTE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG)

run-local:
	docker run \
	--add-host=host.docker.internal:host-gateway \
	-e MYSQL_HOST=host.docker.internal \
	-e MYSQL_PWD=$(MYSQL_PWD) \
	-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
	-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
	$(REMOTE_REPOSITORY)/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: build push run run-local
