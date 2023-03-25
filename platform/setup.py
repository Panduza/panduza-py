from setuptools import setup, find_packages
from setuptools.command.install import install
from panduza_platform.conf import PLATFORM_VERSION

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

setup(
    name="panduza_platform",

    version=PLATFORM_VERSION,

    author="Panduza Team",

    author_email="panduza.team@gmail.com",

    description='Panduza Python Platform',

    long_description="Panduza service that provides support to create drivers that match Panduza specifications",

    packages=find_packages(),

    cmdclass={'install': CustomInstallCommand},

    install_requires=[
        'aardvark-py>=5.40',
        'colorama>=0.4.6',
        'loguru>=0.6.0',
        'paho-mqtt>=1.6.1',
        'pyftdi>=0.54.0',
        'pymodbus>=3.2.0',
        'pyserial>=3.5',
        'pyudev>=0.24.0',
        'pyusb>=1.2.1',
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ]
)
