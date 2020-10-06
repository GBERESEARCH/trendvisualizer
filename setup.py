import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'trendbarometer'
AUTHOR = '...'
AUTHOR_EMAIL = '...'
URL = 'https://github.com/GBERESEARCH/trendbarometer'

LICENSE = 'MIT'
DESCRIPTION = 'Measure which markets are more strongly trending and visualize.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      	'numpy'
	'requests'
	'pandas'
	'matplotlib'
	'norgatedata'
	'yahoofinancials'
	'talib-binary'
	'spyder'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )

