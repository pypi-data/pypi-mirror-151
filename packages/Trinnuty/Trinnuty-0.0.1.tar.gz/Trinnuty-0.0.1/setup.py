from setuptools import setup, find_packages
from Trinnuty.__init__ import __version__
appSettings = {
    "Version": '0.0.1',
    "Description": "Matrix Mathematics and Visualization",
    "Long_Description": '''A work in progress. This will never be the fastest module, but should provide some pretty good looking and easy to use visualizations for mathematical matrix operations.'''
}

setup(
    name='Trinnuty',
    version=__version__,
    packages=find_packages(),
    author="IglooDevelopment",
    long_description_content_type="text/markdown",
    long_description=appSettings["Long_Description"],
    install_requires=[
        'pandas',
        'matplotlib',
        'plotly',
        'numpy',
        'sqlaclhemy',
        'sqlite3'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)