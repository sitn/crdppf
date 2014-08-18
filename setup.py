# -*- coding: utf-8 -*-

try:    
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    
setup(
    name='crdppfportal',
    version='1.0',
    description='sitn, a crdppf project',
    author='sitn',
    author_email='sitn@ne.ch',
    url='http://www.camptocamp.com/geospatial-solutions',
    install_requires=[
        'crdppf_core'
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'paste.app_factory': [
            'main = crdppfportal:main',
        ],
    },
)