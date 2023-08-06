from setuptools import setup

setup(
   name='newArithmeticpkg1239',
   version='0.1.1',
   author='I.P.M',
   author_email='myemail@example.com',
   packages=['newArithmeticpkg1239'],
   scripts=[],
   url='http://pypi.python.org/pypi/newArithmeticpkg1239/',
   license='LICENSE',
   description='my arithmetic package',
   long_description=open('README.md').read(),
   install_requires=[
       "Django >= 1.1.1",
       "pytest"
   ],
)
