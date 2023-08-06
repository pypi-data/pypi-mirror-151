from setuptools import setup, find_packages
import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]
setup(
    name='cgelib',
    version='0.7.2',
    url='https://bitbucket.org/genomicepidemiology/cge_package',
    author='Center for Genomic Epidemiology',
    author_email='food-cgehelp@dtu.dk',
    description='Description of my package',
    packages=find_packages(),
    install_requires=['python-dateutil', 'GitPython'],
)
