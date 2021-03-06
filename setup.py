from setuptools import find_packages, setup

from links import __version__

setup(
    name='clean-architecture-python',
    version=__version__,
    packages=find_packages(exclude=['tests*']),
    package_dir={'links': 'links'},
    url='https://github.com/shudgston/clean-architecture-python',
    license='',
    author='Sean Hudgston',
    author_email='sean.hudgston@gmail.com',
    description='A trivial bookmark manager using "clean architecture"',
    install_requires=[
        'CouchDB==1.1',
        'python-dateutil==2.6.0',
        'passlib==1.7.1',
    ]
)
