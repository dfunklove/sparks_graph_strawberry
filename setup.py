#!/usr/bin/env python

from setuptools import setup

setup(name='sparks_graph',
    version='1.0',
    python_requires='>=3.9',
    author='Daniel Lovette',
    author_email='dfunklove@gmail.com',
    url='https://github.com/dfunklove/sparks_graph',
    license='LICENSE.txt',
    description='GraphQL back-end for Sparksync',
    long_description=open('README.md').read(),
    packages=['sparks_graph'],
    install_requires=['django', 'django-cors-headers', 'django-extensions', 'django-use-email-as-username', 'strawberry-graphql-django', 'strawberry-django-plus', 'strawberry-django-jwt']
    )
