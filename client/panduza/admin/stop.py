import subprocess


def stop(args):

    if args.stopall:
        command = 'docker compose stop mosquitto'
        process = subprocess.Popen(command, shell=True, cwd=args.directory_path)
        process.wait()

    command = 'docker compose stop panduza-py-platform'
    process = subprocess.Popen(command, shell=True, cwd=args.directory_path)
    process.wait()

