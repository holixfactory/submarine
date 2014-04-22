from distutils.core import setup
from submarine import __version__

setup(
    name='submarine',
    version=__version__,
    author='Jongho Lee',
    author_email='jhlee@tntcrowd.com',
    packages=['submarine'],
    url='http://github.com/tntcrowd/submarine',
    license='BSD',
    description='Python 2 / 3 compatible subtitle converter',
    long_description=open('README.md').read(),
)
