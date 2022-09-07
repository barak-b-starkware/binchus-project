from setuptools import setup, find_packages


setup(
    name = 'binchus-project',
    version = '0.1.0',
    author = 'Barak Basson',
    description = 'A project in Dan Gittik\'s course.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest'],
)
