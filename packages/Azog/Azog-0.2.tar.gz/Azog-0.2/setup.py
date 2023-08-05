from setuptools import setup, find_packages

setup(
    long_description=open("README.rst").read(),
    name='Azog',
    version='0.2',
    author="bitex47",
    author_email="xyjy5247@gmail.com",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'paramiko >= 2.10.1',
    ],
)
