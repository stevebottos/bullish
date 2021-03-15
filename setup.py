import glob
import os
from setuptools import setup

req_file = 'requirements.txt'
rel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(rel_path, req_file), "r") as fh:
    requirements = fh.readlines()

# Write the project path for the config
package_root = os.path.join(rel_path, "bullish")
with open(os.path.join(package_root, "package_root"), "w+") as f:
  f.write(package_root)

setup(name='Bullish',
    version="0.0.2",
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
        'bullish', 'bullish.util'
    ],
    data_files=[
      (('bullish/package_root', glob.glob('bullish/package_root'))),
    ]
    )