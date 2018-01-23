# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from setuptools import setup


setup(
    name='hydra-sdk',
    description='Go Hydra SDK for Python',
    keywords='hydra oauth2 openid go',
    version='0.9.0',
    packages=['hydra'],
    install_requires=[
        'pycrypto==2.6.1',
        'python-jose==1.3.2',
        'requests==2.18.1',
    ],
    author='O.S. Systems Software LTDA',
    author_email='contato@ossystems.com.br',
    url='http://www.ossystems.com.br',
    license='MIT',
    zip_safe=True,
)
