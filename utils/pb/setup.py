from setuptools import setup, find_packages

setup(
    name='grpc_stubs',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'grpcio',
        'protobuf',
    ],
)
