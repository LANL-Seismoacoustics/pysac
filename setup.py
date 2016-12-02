try:
    import setuptool
except:
    pass

import os
import os.path
import sys
import commands
from glob import glob
from distutils.core import setup, Extension

setup(name = 'pysac',
      version = '0.2.0',
      description = 'Python interface to the Seismic Analsys Code file format.',
      author = 'J. MacCarthy',
      author_email = 'jkmacc@lanl.gov',
      long_description = '''
Python interface to the Seismic Analsys Code file format.
''',
       packages = ['pysac'],
       py_modules = ['pysac.header', 'pysac.util', 'pysac.arrayio',
                     'pysac.sactrace'],
)
