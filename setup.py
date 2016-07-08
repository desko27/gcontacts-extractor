"""Usage: setup.py [--release] [--zip] [--only-clean-up]

Options:
  -h --help
  -r --release     include everything that is required to get a release
  -z --zip         output a zip package too
  --only-clean-up  perform a clean up of the previous build in dist
"""

import sys
import py2exe
import re

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
if exists('dist/output'): rmtree('dist/output')
for file in glob(join('dist', '*.zip')): remove(file)
if (args['--only-clean-up'] or args['--release']) and exists('dist/settings'): rmtree('dist/settings')
if args['--only-clean-up']: exit()

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

# prepare release: copy settings
if args['--release']:

    makedirs('dist/settings')

    for file in glob(join('settings', '*.sample')):
        copy(file, 'dist/settings/')

    # remove `sample` extension from the copied file settings
    for file in glob(join('dist/settings', '*.sample')):
        rename(file, file.replace('.sample', ''))

# deploy a zip file
if args['--zip']:

    # get version from the script headers
    with open(target, 'r') as f_target:
        content = f_target.read()
        version = re.search('Version:\s*([\d.]+)', content, re.M).group(1)

    # make the zip
    zip_filename = 'gcontacts-extractor-%s' % version
    make_archive(zip_filename, 'zip', 'dist/')
    move(zip_filename + '.zip', 'dist/')
