# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:27:50 2019

@author: arwen
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(["hello.pyx","class_block.pyx"], annotate=True)
)