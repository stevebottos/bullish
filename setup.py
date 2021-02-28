import glob
import os
from setuptools import setup

from bullish import constants 

req_file = 'requirements.txt'
rel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(rel_path, req_file), "r") as fh:
    requirements = fh.readlines()

for path in list(constants.PATHS.values()):
    if not os.path.exists(path):
        os.mkdir(path)

setup(name='Bullish',
    version=0.1,
    author='Steve Bottos',
    author_email='bottos.steve@alwaysai.co',
    url=None,
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
      [console_scripts]
      bullish=bullish.entry_point:bullish
    ''',
    packages=[
        'bullish',
    ],
    data_files=[
      ('bullish/data', glob.glob('bullish/data/*'))
    ])