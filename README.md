# Panduza Python

## Prerequisites

- Windows or Linux
- python3
- pip 

## Requirements
```
sudo apt-get update
sudo apt-get install -y mosquitto git
sudo apt-get install -y python3 python3-pip
pip install "git+https://github.com/Panduza/panduza-py.git"
sudo pip install -r ./tests/requirements.txt
sudo pip install -r ./platform/requirements.txt
sudo pip install ./client/
```

## Client and Admin Tools Installation

```
sudo python3 ./platform/panduza_platform/__main__.py
```
Or
```
sudo local/platform-dryrun.sh
```
## Tests

```
sudo python3 tests/py_tests/test1.py
sudo python3 tests/py_tests/test2.py
```
