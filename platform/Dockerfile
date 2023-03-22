FROM ubuntu:22.04

# Attach to the repository
LABEL org.opencontainers.image.source https://github.com/Panduza/panduza-py
# Argument
ARG PZA_PY_PLATFORM_MODE
# Install Packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Paris \
    apt-get -y install \
        python3 python3-pip \
        git

# Append udev and libusb for device autodetection
RUN apt-get -y install udev
RUN apt-get -y install libusb-1.0-0

# Pip installations
COPY requirements.txt /setup/requirements.txt
RUN pip3 install -r /setup/requirements.txt

# Repos clone
RUN echo $PZA_PY_PLATFORM_MODE

# Create the mirror directory
RUN mkdir -p /etc/panduza

#
WORKDIR /setup
COPY . /setup/
RUN pip install .
RUN cp -v ./deploy/pza-py-platform-run.py /usr/local/bin/pza-py-platform-run.py

# Allow plugin insertion here
ENV PYTHONPATH="/etc/panduza/plugins/py"

#
WORKDIR /work

# Create the directory for platform plugins
# Then run the platform
CMD mkdir -p /etc/panduza/plugins/py; \
    python3 /usr/local/bin/pza-py-platform-run.py