# %%
from setuptools import setup, find_packages
 # %%
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ADC Python Library',
  version='0.0.1',
  description='A very basic test ',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yang Wu',
  author_email='yang.wu@ontario.ca',
  license='MIT', 
  classifiers=classifiers,
  keywords='a basic function', 
  packages=find_packages(),
  install_requires=[''] 
)