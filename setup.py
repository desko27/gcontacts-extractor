"""Usage: setup.py [-k] [-c]

Options:
  -h --help
  -k --keep-settings
  -c --clean-up
"""

import sys
import py2exe

from docopt import docopt
from distutils.core import setup
from shutil import rmtree, copy, move, make_archive
from os.path import exists, join
from os import rename, remove, makedirs, walk
from glob import glob

# retrieve arguments
args = docopt(__doc__)

# clean up previous build
if exists('dist/gcontacts-extractor.exe'): remove('dist/gcontacts-extractor.exe')
if exists('dist/gcontacts-extractor.zip'): remove('dist/gcontacts-extractor.zip')
if exists('dist/library.zip'): remove('dist/library.zip')
if exists('dist/output'): rmtree('dist/output')
if not args['--keep-settings'] and exists('dist/settings'): rmtree('dist/settings')
if args['--clean-up']: exit()

# py2exe compile options
target = 'gcontacts-extractor.py'
sys.argv = [sys.argv[0]] + ['py2exe', '-q']
options = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 1,
        'dll_excludes': ['w9xpopen.exe']
    }
}

# make the exe!
setup(console = [target], options = options)

# copy settings
if not args['--keep-settings']:

	makedirs('dist/settings')

	for file in glob(join('settings', '*.sample')):
	    copy(file, 'dist/settings/')

	# remove `sample` extension from the copied file settings
	for file in glob(join('dist/settings', '*.sample')):
		rename(file, file.replace('.sample', ''))

# deploy zip file
make_archive('gcontacts-extractor', 'zip', 'dist/')
move('gcontacts-extractor.zip', 'dist/')
