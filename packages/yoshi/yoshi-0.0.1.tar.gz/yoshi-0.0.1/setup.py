from setuptools import setup, find_packages
from myapp import __VERSION__


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='yoshi',
    version=__VERSION__,
    description='my first app for pypi',
    entry_points={
        "console_scripts": [
            "myapp = myapp.myapp:main"
        ]
    },
    long_description=readme,
    author='Yoshimasa Yuri',
    author_email='yurimore.tm@gmail.com',
    url='https://github.com/liLy-1905/myapp',
    license=license_txt,
    packages=find_packages(exclude=('sample',))
)
