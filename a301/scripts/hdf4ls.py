"""
dump datasets and global attributes for
an hdf4 file 

example:  python hdf4ls.py filename.hdf

or after installation

hdf4ls filename.hdf
"""

import pprint
import os, sys
import argparse
from pathlib import Path
from pyhdf.SD import SD, SDC

def hdf4ls(filename):
    """
    Read the SDS datasets and global attributes of an hdf4 file

    Parameters
    ----------

    filename: str or Path object
        hdf4 file to read

    Returns
    -------
 
    prints the metadata

    """
    the_file = SD(str(filename), SDC.READ)
    stars='*'*50
    print((f'\n{stars}\nReading {filename}\n'
           f'\nnnumber of datasets, number of attributes\n'
           f'={the_file.info()}\n{stars}\n'))
    datasets_dict = the_file.datasets()
    print(f'\n{stars}\nHere are the datasets\n{stars}\n')
    for idx,sds in enumerate(datasets_dict.keys()):
        print(idx,sds)

    print(f'\n{stars}\nHere are the truncated global attributes\n{stars}\n')
    for key, value in the_file.attributes().items():
        print_value=str(value)
        if len(print_value) > 100:
            print_value=print_value[:100]
        print(f'Key: {key} --- Value: {print_value}')

def make_parser():
    """
    set up the command line arguments needed to call the program
    """
    linebreaks = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=linebreaks, description=__doc__.lstrip())
    parser.add_argument("filename", type=str,help='name of hdf4 file')
    return parser
            

def main(args=None):
    """
    args: optional -- if missing then args will be taken from command line
          or pass [h4_file] -- list with name of h4_file to open
    """
    parser = make_parser()
    parsed_args = parser.parse_args(args)
    file_path = Path(parsed_args.filename).resolve()      
    hdf4ls(file_path)

if __name__ == "__main__":
    #
    # will exit with non-zero return value if exceptions occur
    #
    #args = ['vancouver_hires.h5']
    sys.exit(main())
