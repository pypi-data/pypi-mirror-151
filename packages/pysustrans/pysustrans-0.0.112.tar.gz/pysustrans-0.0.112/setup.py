from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent.resolve()
long_description = (this_directory / "README.md").read_text(encoding="utf8")

# Details
PACKAGE_NAME = 'pysustrans'
AUTHOR = 'Rahul Raoniar'
EMAIL = "rahul.raoniar@outlook.com"
URL = 'https://github.com/rahul-raoniar/pysustrans'
DOWNLOAD_URL = 'https://pypi.org/project/pysustrans/'
VERSION = "0.0.112"
DESCRIPTION = 'pysustran is a statistical Python package for Transportation data analysis.'
LONG_DESCRIPTION = long_description
LICENSE = 'MIT'
CLASSIFIERS = [
        'Programming Language :: Python :: 3'
]

LONG_DESC_TYPE = "text/markdown"


# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn'],
    classifiers= CLASSIFIERS,
    python_requires=">=3.8"
)

