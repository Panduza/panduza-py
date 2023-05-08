import argparse


from .hunt import hunt
from .start import start
from .stop import stop
from .setup import setup
from .scan import scan
from .init_directory import init_directory



def pzadmin_main():

    parser = argparse.ArgumentParser(description='Panduza Admin Helper')
    parser.add_argument('command', metavar='command', type=str,
                        choices=["init", "hunt", "start", "stop", "setup", "scan"],
                        help='command to execute')
    parser.add_argument('directory_path', metavar='directory_path', type=str,
                        default='.', nargs='?',
                        help='path to the directory')
    parser.add_argument('-d', dest='deamon', action='store_true',
                        help='for the command "start", the platform is started in background')
    parser.add_argument('--stop-all', dest='stopall', action='store_true',
                        help='for the command "stop", mosquitto is also stopped')

    args = parser.parse_args()

    # print(f'Command             : {args.command}')
    # print(f'Working directory   : {args.directory_path}')

    if args.command == "init":
        init_directory(args)
    elif args.command == "hunt":
        hunt(args.directory_path)
    elif args.command == "start":
        start(args)
    elif args.command == "stop":
        stop(args)
    elif args.command == "setup":
        setup(args)
    elif args.command == "scan":
        scan(args)
    else:
        print(f'Invalid arguments provided for pzadmin.')

