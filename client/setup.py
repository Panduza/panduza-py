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

        install_requires=['setuptools', 'paho-mqtt', 'python-magic', 'colorama', 'robotframework-pythonlibcore'],

        entry_points={
            'console_scripts': [
                'pzadmin=panduza.admin.pzadmin:pzadmin_main',
            ],
        },

        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            'Operating System :: POSIX',
        ]
)

