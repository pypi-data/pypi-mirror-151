# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='flexolink',
    version='1.0.1',
    description=(
        'hello hello hello, '
        'ko ko ko.'
    ),
    long_description=open('README.md').read(),
    author='huwei',
    author_email='hwboot@163.com',
    maintainer='Wei Hu',
    maintainer_email='hwboot@163.com',
    license='Flexolink License',
    platforms=["linux"],
    url='https://gitee.com/huweiko/flexolink',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'flexolink = flexolink.main:main',
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3',
    install_requires=[
	'numpy',
	'scipy'
    ]
)
