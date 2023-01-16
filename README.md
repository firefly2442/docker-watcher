# docker-watcher

A Docker container that examines the local Docker install and tries to pull updated
images as well as save images to a registry.  It also automatically cleans
up any dangling images.  This can help with maintaining
synchronization of images across multiple machines in a local network.

## Requirements

* Docker
* docker-compose

## Setup

Create a `.env` file and specify the following:

```file
DOCKER_REGISTRY="192.168.1.226:5000/"
```

This will be the location where it will look to store all local images.

Edit `/etc/docker/daemon.json` and add entries for the registry

```file
{
    "insecure_registries": ["192.168.1.226:5000"]
}
```

Then restart Docker

## Building

```shell
docker compose build --pull
```

## Running

```shell
docker compose up -d
```

## Docker Debugging

```shell
docker exec -it <id> bash
```

## Docker Teardown

```shell
docker compose down -v
```

## References
