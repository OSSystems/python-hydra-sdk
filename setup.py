# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from setuptools import setup


setup(
    name='hydra-sdk',
    description='Go Hydra SDK for Python',
    keywords='hydra oauth2 openid go',
    version='0.1-dev',
    packages=['hydra'],
    install_requires=[
        'pycrypto',
        'python-jose',
        'requests',
    ],
    author='O.S. Systems Software LTDA',
    author_email='contato@ossystems.com.br',
    url='http://www.ossystems.com.br',
    license='MIT',
    zip_safe=True,
)
