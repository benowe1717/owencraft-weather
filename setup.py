#!/usr/bin/env python3
"""Project Setup"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    readme: str = file.read()

with open('LICENSE', 'r', encoding='utf-8') as file:
    my_license: str = file.read()

setup(
    name='owencraft-weather',
    version='1.0.0',
    description='Control the weather on the Owencraft Minecraft Server',
    long_description=readme,
    author='Benjamin Owen',
    author_email='benjamin@projecttiy.com',
    url='https://github.com/benowe1717/owencraft-weather',
    license=my_license,
    packages=find_packages(exclude=('tests', 'docs'))
)
