from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.3'
DESCRIPTION = 'A package for controlling the motor driver'

# Setting up
setup (
    name="motordriverpkg",
    version=VERSION,
    author="saravana kannan",
    author_email="saravana.rae@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyserial'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)