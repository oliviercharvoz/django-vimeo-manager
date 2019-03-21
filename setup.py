import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-vimeo-manager',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPLv3 License',
    description='A simple Django app that adds a layer on top of the Vimeo API.',
    long_description=README,
    url='https://olivier.charvoz.eu/',
    author='Olivier Charvoz',
    author_email='olivier@charvoz.eu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPLv3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'PyVimeo',
    ],
)
