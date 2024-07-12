# mr_dns_tool/setup.py

from setuptools import setup, find_packages

setup(
    name='mr_dns',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'dnspython',
        'whois'
    ],
    entry_points={
        'console_scripts': [
            'mr_dns=mr_dns.mr_dns:main',
        ],
    },
    author='Zahir Shah',
    author_email='shah.zahir54@gmail.com',
    description='A tool to gather domain information',
    url='https://github.com/s-zahir/mr_dns.git',
)
