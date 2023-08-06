from distutils.core import setup

from setuptools import find_packages

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from ed_analytics.consts import AUTHOR, AUTHOR_EMAIL, DESCRIPTION, MAINTAINER, MAINTAINER_EMAIL, NAME, VERSION


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,

    url="https://github.com/skylartown/ed-analytics.py",

    license="MIT",
    keywords=[
        "education",
        "analytics",
        "classroom"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Intended Audience :: Education"
    ],
    package_dir={'': "."},
    packages=find_packages("."),
    python_requires=">=3.6"
)
