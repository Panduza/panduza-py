import os
import json
from pathlib import Path
from dataclasses import dataclass

from .writer_env_file import EnvFileWriter
from .writer_mosquitto_conf import MosquittoConfWriter


@dataclass
class DockerComposeWriter:
    filepath: str

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
    image: ghcr.io/panduza/panduza-py-platform:latest
    # To use your local platform build
    # image: local/panduza-py-platform
    privileged: true
    network_mode: host
    user: "${UID}:${GID}"
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







def init_directory(args):
    os.makedirs(args.directory_path, exist_ok=True)
    os.makedirs(Path(args.directory_path) / 'data', exist_ok=True)
    DockerComposeWriter(Path(args.directory_path) / 'docker-compose.yml').write()
    TreeWriter(Path(args.directory_path) / 'tree.json').write()
    MosquittoConfWriter(Path(args.directory_path) / 'data/mosquitto.conf').write()
    EnvFileWriter(Path(args.directory_path) / '.env').write()
