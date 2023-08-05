from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='wordleimageeditor',
  version='0.0.2',
  description='A module for creating images for Wordle',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Artyom Ulyanov',
  author_email='uljanoff.artem@yandex.ru',
  license='MIT', 
  classifiers=classifiers,
  keywords='wordle', 
  packages=find_packages(),
  install_requires=['pillow'] 
)
