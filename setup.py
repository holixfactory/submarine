from distutils.core import setup
from submarine import __version__

setup(
    name='submarine',
    version=__version__,
    author='Jongho Lee',
    author_email='jhlee@tntcrowd.com',
    packages=['submarine'],
    keywords=['Subtitle', 'SubRip', 'WEBVTT'],
    url='http://github.com/tntcrowd/submarine',
    platform='Cross Platform',
    download_url='https://codeload.github.com/tntcrowd/submarine/legacy.tar.gz/master',
    license='BSD',
    description='Python 2/3 compatible subtitle converter',
    long_description=open('README.md').read(),
)
