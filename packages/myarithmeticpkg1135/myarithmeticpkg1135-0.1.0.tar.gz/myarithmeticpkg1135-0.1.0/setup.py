from setuptools import setup

setup(
   name='myarithmeticpkg1135',
   version='0.1.0',
   author='A.N.F',
   author_email='myemail@example.com',
   packages=['myarithmeticpkg1135'],
   scripts=[],
   url='http://pypi.python.org/pypi/angelnfdes/',
   license='LICENSE',
   description='my arithmetic package',
   long_description=open('README.md').read(),
   install_requires=[
       "Django >= 1.1.1",
       "pytest",
   ],
)