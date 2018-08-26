# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
      name="gomap",
      version="0.1dev",
      packages=["gomap",],
      license="MIT",
      python_requires=">=3.5",
      install_requires=[
              "numpy>=1.14",
              "pandas>=0.23",
              "pillow>=5",
              "bokeh>=0.13"
              ]
      )

