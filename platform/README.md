# Panduza Python Platform

Panduza platform provides a simple way to create MQTT clients that match panduza specifications.

## Recommended Usage => docker

```bash
source docker.build-image.sh
```

```bash
docker run \
    --network host \
    -v $PWD:/etc/panduza \
    -v /run/udev:/run/udev:ro \
    local/panduza-py-platform:latest
```

