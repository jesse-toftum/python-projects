from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("color_text_cython.pyx"))