from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(this_directory, 'README.md')

with open(readme_path, encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='daredata_snowconn',
    version='1.0.2',
    description='Python utilities for connection to the Snowflake data '
                'warehouse',
    url='https://github.com/DareData/snowconn',
    author='DareData Engineering',
    author_email='sam@daredata.engineering',
    packages=['daredata_snowconn'],
    install_requires=[
        'wheel==0.32.3',
        'snowflake-sqlalchemy==1.2.3',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
