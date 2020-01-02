from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("image_tests/color_test.pyx", annotate=True))

# To compile, run:
    # python image_tests/cython_build.py build_ext --inplace