import argparse


from .hunt import hunt
from .start import start
from .setup import setup
from .init_directory import init_directory



def pzadmin_main():

    parser = argparse.ArgumentParser(description='Panduza Admin Helper')
    parser.add_argument('command', metavar='command', type=str,
                        choices=["init", "hunt", "start", "stop", "setup"],
                        help='command to execute')
    parser.add_argument('directory_path', metavar='directory_path', type=str,
                        default='.', nargs='?',
                        help='path to the directory')

    args = parser.parse_args()

    print(f'Command             : {args.command}')
    print(f'Working directory   : {args.directory_path}')

    if args.command == "init":
        init_directory(args)
    elif args.command == "hunt":
        hunt(args.directory_path)
    elif args.command == "start":
        start(args.directory_path)
    elif args.command == "stop":
        print(f'Stopping to process directory: {args.directory_path}')
    elif args.command == "setup":
        setup(args)
    else:
        print(f'Invalid arguments provided for pzadmin.')

