from setuptools import setup, find_packages
import codecs
import os

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


# Setting up
setup(
    name = 'read_comports_tonet',
    version = "0.0.1",
    author = "Yosia Lukumai",
    author_email = "yosialukumai@gmail.com",
    url ='https://github.com/yosiaLukumai/Reading-data-From-Ports',
    description ="Easy read data from COM ports and send them over the server(net) example in your arduino or raspberrypi project",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = "MIT",
    install_requires = ['requests >=2.20.0 ', 'schedule >= 1.0.0', 'pyserial >= 3.0'],
    packages=find_packages(),
    keywords=['python', 'read com ports', 'read com ports data send to net', 'read com data and send to thingsspeak', 'proteus data to server', 'arduino to server', 'rasberrypi to server'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)



