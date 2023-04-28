import os
import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DockerComposeWriter:
    filepath: str

    def write(self):
        text = '''version: '3'
services:

  # docker compose run --service-ports mosquitto
  mosquitto:
    image: eclipse-mosquitto
    ports:
      - 1883:1883
      - 9001:9001
    volumes:
      - ./data/mosquitto.conf:/mosquitto/config/mosquitto.conf

  panduza-py-platform:
    # image: ghcr.io/panduza/panduza-py-platform:latest
    # To use your local platform build
    image: local/panduza-py-platform
    privileged: true
    network_mode: host
    environment:
      - HUNT
    volumes:
      - .:/etc/panduza
      - /run/udev:/run/udev:ro
    # command: bash
    '''
        with open(self.filepath, 'w') as f:
            print(f" + Write file '{self.filepath}'")
            f.write(text)



@dataclass
class TreeWriter:
    filepath: str

    def write(self):
        tree = {
            "machine": "rename_this_machine",
            "brokers": {
                "rename_this_broker": {
                    "addr": "localhost",
                    "port": 1883,
                    "interfaces": [
                        {
                            "name": "fake_psu",
                            "driver": "py.psu.fake"
                        }
                    ]
                }
            }
        }
        with open(self.filepath, 'w') as f:
            print(f" + Write file '{self.filepath}'")
            f.write(json.dumps(tree, indent=4))





@dataclass
class MosquittoConfWriter:
    filepath: str

    def write(self):
        tree = """
#
allow_anonymous true

#
listener 1883 0.0.0.0

#
listener 9001 0.0.0.0
protocol websockets
        """
        with open(self.filepath, 'w') as f:
            print(f" + Write file '{self.filepath}'")
            f.write(json.dumps(tree, indent=4))


def init_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)
    os.makedirs(Path(directory_path) / 'data', exist_ok=True)
    DockerComposeWriter(Path(directory_path) / 'docker-compose.yml').write()
    TreeWriter(Path(directory_path) / 'tree.json').write()
    MosquittoConfWriter(Path(directory_path) / 'data/mosquitto.conf').write()

