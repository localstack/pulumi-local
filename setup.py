#!/usr/bin/env python

from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

if __name__ == '__main__':

    setup(
        name='pulumi-local',
        version='1.2',
        description='Thin wrapper script to use Pulumi with LocalStack',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='LocalStack Team',
        author_email='info@localstack.cloud',
        url='https://github.com/localstack/pulumi-local',
        packages=[],
        scripts=['bin/pulumilocal', 'bin/pulumilocal.bat'],
        package_data={},
        data_files={},
        install_requires=[],
        license="Apache License 2.0",
        classifiers=[
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
