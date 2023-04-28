import argparse


from .hunt import hunt
from .start import start
from .init_directory import init_directory



def pzadmin_main():

    parser = argparse.ArgumentParser(description='Panduza Admin Helper')
    parser.add_argument('directory_path', metavar='directory_path', type=str,
                        default='.',
                        help='path to the directory')
    parser.add_argument('--init', dest='init', action='store_true',
                        help='initialize the directory')
    parser.add_argument('--hunt', dest='hunt', action='store_true',
                        help='start hunting in the directory')
    parser.add_argument('--start', dest='start', action='store_true',
                        help='start processing in the directory')
    parser.add_argument('--stop', dest='stop', action='store_true',
                        help='stop processing in the directory')

    args = parser.parse_args()

    print(f'Working directory: {args.directory_path}')

    if args.init:
        init_directory(args.directory_path)
    elif args.hunt:
        hunt(args.directory_path)
    elif args.start:
        start(args.directory_path)
    elif args.stop:
        print(f'Stopping to process directory: {args.directory_path}')
    else:
        print(f'Invalid arguments provided for pzadmin.')
