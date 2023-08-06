#
# setup.py
#
# Copyright (C) 2019-2021 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
#
# This file is part of fattura-elettronica-reader.
#
# fattura-elettronica-reader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fattura-elettronica-reader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fattura-elettronica-reader.  If not, see <http://www.gnu.org/licenses/>.
#
"""setup."""

from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='fattura_elettronica_reader',
    version='3.0.2',
    packages=find_packages(exclude=['*tests*']),
    license='GPL',
    description='A utility that is able to check and extract electronic invoice received from the Sistema di Interscambio.',
    long_description=readme,
    long_description_content_type='text/markdown',
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@tutanota.com',
    keywords='invoice reader SDI',
    url='https://blog.franco.net.eu.org/software/#fattura-elettronica-reader',
    python_requires='>=3.5,<4',
    entry_points={
        'console_scripts': [
            'fattura_elettronica_reader=fattura_elettronica_reader.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'appdirs>=1.4,<1.5',
        'atomicwrites>=1.4,<2',
        'filetype>=1,<2',
        'fpyutils>=2.1,<3'
        'lxml>=4.6.5,<4.9',
        'PyYAML>=6,<7',
        'requests>=2.27,<3',
    ],
)
