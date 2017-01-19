from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='clim',
    version='1.0.0',
    description='CoLumn IMproved',
    long_description='clim is an improved version of *IX column command. Lets you print any TSV/CSV file in human readable format, with optional frames, and provides regular expressions to extract information from every field. It lets you convert single column files into tables as well.',

    url='https://github.com/coelias/clim',
    author='Carlos del Ojo Elias',
    author_email='deepbit@gmail.com',

    license='GPLv3',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        "Topic :: Scientific/Engineering :: Information Analysis",
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Intended Audience :: Science/Research',

        'Environment :: Console',
    ],

    keywords='csv tsv column human-readable dataset',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'clim=clim.clim:main',
        ],
    },
)
