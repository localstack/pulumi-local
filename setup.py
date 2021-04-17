#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':

    setup(
        name='pulumi-local',
        version='0.1',
        description='Thin wrapper script to use Pulumi with LocalStack',
        author='Waldemar Hummer',
        author_email='waldemar.hummer@gmail.com',
        url='https://github.com/localstack/pulumi-local',
        packages=[],
        scripts=['bin/pulumilocal', 'bin/pulumilocal.bat'],
        package_data={},
        data_files={},
        install_requires=['pyyaml'],
        license="Apache License 2.0",
        classifiers=[
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Software Development :: Testing"
        ]
    )
