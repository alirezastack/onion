from setuptools import setup, find_packages
from onion.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='onion',
    version=VERSION,
    description='Your Service Description',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Sayyed Alireza Hoseini',
    author_email='alireza.hosseini@zoodroom.com',
    url='https://git.zoodroom.com/basket/onion',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'onion': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        onion = onion.main:main
    """,
)
