from setuptools import setup, find_packages

setup(
    name='tempmonitor',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    description='micropython based wireless temperature/humidity monitoring',
    license='GPLv3',
    url='https://github.com/larsks/tempmonitor',
    packages=[
        'dhtmanager',
    ],
    install_requires=[
        'flask',
        'pony',
        'psycopg2',
        'psycopg2cffi'
    ]
)
