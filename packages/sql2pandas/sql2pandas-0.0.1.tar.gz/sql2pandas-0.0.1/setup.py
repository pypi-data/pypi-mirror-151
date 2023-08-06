#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(name="sql2pandas",
      version="0.0.01",
      description="Turn SQL into Pandas Statements",
      license="MIT",
      author="Eugene Wu",
      author_email="ewu@cs.columbia.edu",
      url="http://github.com/cudbg/sql2pandas",
      include_package_data = True,      
      packages = find_packages(),
      package_dir = {'sql2pandas' : 'sql2pandas'},
      scripts = [],
      package_data = { 'sql2pandas' : ['sql2pandas/data/*'] },
      install_requires = [
        'parsimonious', 'pandas', 'numpy',
        'python-dateutil', 'pytest', 'sqlalchemy'
      ],
      keywords= "database pandas engine compiler")
