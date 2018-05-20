"""
Created by adam on 4/28/18
"""
__author__ = 'adam'

if __name__ == '__main__':
    from distutils.core import setup

setup(
    name='TwitterDataAnalysis',
    version='0.1.0',
    author='adm',
    author_email='jrh@example.com',
    packages=[],
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='',
    long_description=open('README.txt').read(),
    install_requires=[
        "ConfigParser",
        "dawg",
        "factory_boy",
        "Faker",
        "ipyparallel",
        "logbook",
        "mysql-connector-python",
        "nltk",
        "progress",
        "sqlalchemy",
        "tornado", 'requests'
    ],
)