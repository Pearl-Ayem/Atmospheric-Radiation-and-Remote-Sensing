from pathlib import Path
#
# open the VERSION file and read it into a301.__version__
# https://github.com/pypa/setuptools/issues/1316
#
__version_file__=Path(__file__).parent / Path('VERSION')
#
#  if __version_file__ doesn't exist, try to create it and
#  write 'no_version', if that doesn't work (no write permission), set
#  __version_file__ to None
#
if not __version_file__.is_file():
    __version__ = 'no_version'
    try:
        with open(__version_file__,'w') as f:
            f.write(__version__)
    except:
        __version_file__=None
else:
    with open(__version_file__) as f:
        __version__=f.read().strip()

