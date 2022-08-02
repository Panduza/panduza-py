# Simple Standalone Test
import sys
import argparse
from panduza import Core
from panduza import File

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', default=None)
parser.add_argument('mime', nargs='?', default=None)
args = parser.parse_args()

# Load Aliases
Core.LoadAliases({
    "local_test": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {
            "file_test": "pza/test/file_fake/file_test"
        }
    }
})

# Create file interface
ff = File(alias="file_test")

# Update content from a file
ff.content.set_from_file(sys.argv[1])

