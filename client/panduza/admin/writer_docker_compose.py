import os
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass



@dataclass
class DockerComposeWriter:
    filepath: str

    def set_dev_mode(self, dev):
        self.__dev = dev

    def write(self):
        text = '''version: '3'
services:

  # docker compose run --service-ports mosquitto
  mosquitto:
    image: eclipse-mosquitto
    user: "${UID}:${GID}"
    ports:
      - 1883:1883
      - 9001:9001
    volumes:
      - ./data/mosquitto.conf:/mosquitto/config/mosquitto.conf

  panduza-py-platform:
    '''
        if not self.__dev:
            text += '''    image: ghcr.io/panduza/panduza-py-platform:latest
    # To use your local platform build
    # image: local/panduza-py-platform
    '''
        else:
            text += '''# image: ghcr.io/panduza/panduza-py-platform:latest
    # To use your local platform build
    image: local/panduza-py-platform
    '''
        text += '''privileged: true
    network_mode: host
    user: "${UID}:${GID}"
    environment:
      - HUNT
    volumes:
      - .:/etc/panduza
      - /run/udev:/run/udev:ro
    # command: bash
'''

        # Write the file
        with open(self.filepath, 'w') as f:
            print(f" + Write file '{self.filepath}'")
            f.write(text)


