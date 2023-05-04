import subprocess




def start(args):

    command = 'docker compose create mosquitto'
    process = subprocess.Popen(command, shell=True, cwd=args.directory_path)
    process.wait()

    command = 'docker compose create panduza-py-platform'
    process = subprocess.Popen(command, shell=True, cwd=args.directory_path)
    process.wait()

    command = 'docker compose start mosquitto'
    process = subprocess.Popen(command, shell=True, cwd=args.directory_path)
    process.wait()


    command = None
    if args.deamon:
        command = 'docker compose start panduza-py-platform'
    else:
        command = 'docker compose run panduza-py-platform'
    process = subprocess.Popen(command, shell=True, cwd=args.directory_path)
    process.wait()


