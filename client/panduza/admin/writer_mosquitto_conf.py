import os
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class MosquittoConfWriter:
    filepath: str

    def write(self):
        content = """
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
            f.write(content)

