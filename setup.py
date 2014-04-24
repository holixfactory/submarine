from distutils.core import setup
from submarine import __version__

setup(
    name='submarine',
    version=__version__,
    author='Jongho Lee',
    author_email='jhlee@tntcrowd.com',
    packages=['submarine'],
    keywords=['Subtitle', 'SAMI', 'SubRip', 'WEBVTT', 'Converter'],
    url='http://github.com/tntcrowd/submarine',
    platforms='Cross Platform',
    download_url='https://codeload.github.com/tntcrowd/submarine/legacy.tar.gz/master',
    license='BSD',
    description='Python 2/3 compatible subtitle converter',
    long_description=open('README.rst').read(),
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    entry_points={'console_scripts': ['submarine = submarine.submarine:main']},
)
