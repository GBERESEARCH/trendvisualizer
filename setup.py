from setuptools import setup

setup(name='tools',
      version='0.0.1',
      description='EDA Tools',
      author='...',
      author_email='...',
      packages=['tools'],
      install_requires=['norgatedata',
                        'requests',
			'pandas',
                        'numpy',
                        'matplotlib',
                        'talib',
                        'time',
                        'functools',
			'yahoofinancials'])

