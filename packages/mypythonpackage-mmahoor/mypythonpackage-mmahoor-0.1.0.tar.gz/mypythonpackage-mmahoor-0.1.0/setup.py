from setuptools import setup

setup(
   name='mypythonpackage-mmahoor',
   version='0.1.0',
   author='M.H.M',
   author_email='myemail@example.com',
   packages=['mypythonpackage-mmahoor'],
   scripts=[],
   url='http://pypi.python.org/pypi/mypythonpackage-mmahoor/',
   license='LICENSE.txt',
   description='hello world',
   long_description=open('README.md').read(),
   install_requires=[
       "Django >= 1.1.1",
       "pytest",
   ],
)
