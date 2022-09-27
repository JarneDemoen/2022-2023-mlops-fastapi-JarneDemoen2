#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Nathan Segers",
    author_email='nathan.segers@howest.be',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Boilerplate to start with a FastAPI project in the 1st class of MLOps",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fastapi_boilerplate',
    name='fastapi_boilerplate',
    packages=find_packages(include=['fastapi_boilerplate', 'fastapi_boilerplate.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/NathanSegers/fastapi_boilerplate',
    version='0.1.0',
    zip_safe=False,
)
