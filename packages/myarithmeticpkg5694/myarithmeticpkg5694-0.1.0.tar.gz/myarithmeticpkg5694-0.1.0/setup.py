from setuptools import setup

setup(
   name='myarithmeticpkg5694',
   version='0.1.0',
   author='M.H.M',
   author_email='myemail@example.com',
   packages=['myarithmeticpkg5694'],
   scripts=[],
   url='http://pypi.python.org/pypi/mmahoor/',
   license='LICENSE',
   description='my arithmetic package',
   long_description=open('README.md').read(),
   install_requires=[
       "Django >= 1.1.1",
       "pytest",
   ],
)
