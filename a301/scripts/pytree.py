"""
walk a path
"""

import os, sys
import argparse

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def make_parser():
    """
    set up the command line arguments needed to call the program
    """
    linebreaks = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=linebreaks, description=__doc__.lstrip())
    parser.add_argument("--startin","-s", type=str, default=".",help='path to folder, defaults to cwd')
    return parser
            

def main(args=None):
    """
    args: optional -- if missing then args will be taken from command line
          or pass [h4_file] -- list with name of h4_file to open
    """
    parser = make_parser()
    parsed_args = parser.parse_args(args)
    startpath = parsed_args.startin
    list_files(startpath)

if __name__ == "__main__":
    #
    # will exit with non-zero return value if exceptions occur
    #
    #args = ['vancouver_hires.h5']
    sys.exit(main())
