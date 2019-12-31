import os
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("cython_tests/helloworld.pyx"))

# os.system("python build_cython.py build_ext --inplace")
