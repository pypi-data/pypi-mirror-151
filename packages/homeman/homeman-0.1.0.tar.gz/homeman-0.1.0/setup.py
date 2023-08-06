from setuptools import setup, find_packages

setup(
    name = 'homeman',
    version = '0.1.0',
    description = 'keep files synchronized between user home and your special home directory',
    author = 'sunn4room',
    author_email = 'sunn4room@163.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'homeman = homeman:main'
        ]
    }
)
