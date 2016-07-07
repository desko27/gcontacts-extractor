import sys
from distutils.core import setup
import py2exe

entry_point = sys.argv[1]
sys.argv.pop()
sys.argv.append('py2exe')
sys.argv.append('-q')

opts = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 1
    }
}

setup(console=[entry_point], options=opts, zipfile=None)
