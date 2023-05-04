import os
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass



def get_id_u():
    command = 'id -u'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    return out.decode('utf-8')

def get_id_g():
    command = 'id -g'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    return out.decode('utf-8')


@dataclass
class EnvFileWriter:
    filepath: str

    def write(self):
        content = f"""
        UID={get_id_u()}
        GID={get_id_g()}
        """
        with open(self.filepath, 'w') as f:
            print(f" + Write file '{self.filepath}'")
            f.write(content)

