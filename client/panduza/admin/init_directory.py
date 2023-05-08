import os
import json
from pathlib import Path
from dataclasses import dataclass

from .writer_tree import TreeWriter
from .writer_env_file import EnvFileWriter
from .writer_mosquitto_conf import MosquittoConfWriter
from .writer_docker_compose import DockerComposeWriter


def init_directory(args):
    os.makedirs(args.directory_path, exist_ok=True)
    os.makedirs(Path(args.directory_path) / 'data', exist_ok=True)

    dcw = DockerComposeWriter(Path(args.directory_path) / 'docker-compose.yml')
    dcw.set_dev_mode(args.dev)
    dcw.write()

    TreeWriter(Path(args.directory_path) / 'tree.json').write()
    MosquittoConfWriter(Path(args.directory_path) / 'data/mosquitto.conf').write()
    EnvFileWriter(Path(args.directory_path) / '.env').write()

