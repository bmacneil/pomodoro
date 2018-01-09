try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
config = {
    'description': 'My Project',
    'author': 'Brad MacNeil',
    'url': 'URL to get it',
    'download_url': 'URL to download it',
    'author_email': 'My Email',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pomodoro'],
    'scripts': [],
    'name': 'pomodoro'
}

setup(**config)
