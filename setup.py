#!/usr/bin/env python


from setuptools import setup, find_packages
import sys

install_requires = [
    'lz4tools',
]

setup(
    name="lz4-container",
    version="1.0.0",
    description="lz4 container",
    classifiers=[],
    author="xp.xu",
    install_requires=install_requires,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    scripts=['scripts/lz4'],
    zip_safe=True,
    entry_points=""
)
