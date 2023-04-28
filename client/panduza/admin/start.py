import subprocess


def start(directory_path):

    command = 'docker compose create mosquitto'
    process = subprocess.Popen(command, shell=True, cwd=directory_path)
    process.wait()

    command = 'docker compose create panduza-py-platform'
    process = subprocess.Popen(command, shell=True, cwd=directory_path)
    process.wait()

    command = 'docker compose start mosquitto'
    process = subprocess.Popen(command, shell=True, cwd=directory_path)
    process.wait()

    command = 'docker compose start panduza-py-platform'
    process = subprocess.Popen(command, shell=True, cwd=directory_path)
    process.wait()

