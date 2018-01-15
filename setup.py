#!/usr/bin/env python
"""Setup script for the project."""

from setuptools import setup

VERSION = '0.0.1'

setup(
    author='Team per la Trasformazione Digitale',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    description='Sphinx extension that embeds Discourse threads in documents.',
    install_requires=['sphinx'],
    keywords='sphinx discourse',
    license='BSD-3-clause',
    name='sphinxcontrib-discourse',
    package_data={},
    packages=['sphinxcontrib'],
    version=VERSION,
    zip_safe=False,
)
