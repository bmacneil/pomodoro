#!/usr/bin/python3
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
config = {
    'description': 'A pomodoro program with a simple gui to track work sessions.',
    'author': 'Brad MacNeil',
    'url': 'URL to get it',
    'download_url': 'URL to download it',
    'author_email': 'My Email',
    'version': '0.2',
    'install_requires': ['schedule', 'tinydb', 'ujson'],
    'python_requires': '>=3',
    'packages': ['pomodoro'],
    'scripts': [],
    'name': 'pomodoro',
    'entry_points': {'console_scripts': ['pomodoro=pomodoro:main']}
}

setup(**config)
