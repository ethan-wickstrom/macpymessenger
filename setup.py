# -*- coding: utf-8 -*-
from setuptools import setup
from os.path import join, dirname

with open (join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = f.read().split("\n")

setup(
    name='iPyMessenger',
    version='0.1.0',
    url='https://github.com/ethan-wickstrom/iPyMessenger',
    author='Ethan Wickstrom',
    author_email='e.t.wickstrom@wustl.edu',
    description="Support for sending/receiving iMessages",
    packages=['py_imessage'],
    zip_safe=False,
    python_requires='>=3',
    include_package_data=True,
    platforms='Operating System :: MacOS :: MacOS X',
    install_requires=install_requires,
    tests_require=[
        'nose'
    ],
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)