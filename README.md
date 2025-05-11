# Panduza Python

## Prerequisites

- Windows or Linux
- python3
- pip 

## Tests

```bash
behave -v --no-capture --color --no-logcapture
```


## Flat Buffers

```bash
# 
./flatc.exe --python -o panduza/fbs/ panduza/fbs/notification_v0.fbs
# 
./flatc.exe --python -o panduza/fbs/ panduza/fbs/status_v0.fbs
```




