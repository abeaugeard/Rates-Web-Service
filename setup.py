
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Rates web service',
    version='0.1.0',
    description='A RESTFul Web Service',
    long_description=readme,
    author='Aurélie Beaugeard',
    author_email='aurelie.beaugeard@insa-rouen.fr',
    url='https://github.com/abeaugeard/Rates-Web-Service.git',
    license=license,
    #packages=find_packages(exclude=('tests', 'docs'))
)
