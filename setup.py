"""Setup script for intelpy"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="intelpy",
    version="1.0.0b",
    description="Don't let bad guys blow up your stuff",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Riifta/intelpy",
    author="Swizzles Saissore",
    author_email="swizzleseve@gmail.com",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["intelpy"],
    include_package_data=True,
    install_requires=[
        "pyqt5", "pathlib", "watchdog", "networkx", "playsound", "pygobject", 'mechanize', 'tornado'
    ],
    entry_points={"console_scripts": ["intelpy=intelpy.__main__:main"]},
)
