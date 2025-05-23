from setuptools import setup, find_packages
from setuptools.command.install import install

# Setting up
setup(
        name="panduza",
        version='0.0.1',
        author="Panduza Team",
        author_email="panduza.team@gmail.com",
        description='Wrapper for Panduza MQTT Calls',
        long_description='This library provides simple wrapper to help implementing tests through panduza interfaces',
        packages=find_packages(),

        install_requires=[
            'setuptools',
            'paho-mqtt==2.1.0',
            'flatbuffers==25.2.10',
            'numpy==2.2.4'
        ],


        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            'Operating System :: POSIX',
        ]
)

