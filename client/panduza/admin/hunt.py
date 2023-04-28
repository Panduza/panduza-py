import subprocess


def hunt(directory_path):

    # set the environment variable
    env = {'HUNT': '1'}

    # run the docker-compose command
    command = 'docker compose run panduza-py-platform'
    process = subprocess.Popen(command, shell=True, env=env, cwd=directory_path)
    process.wait()

