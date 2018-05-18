from setuptools import find_packages, setup

setup(
    name="Common",
    version="1.0.0",
    install_requires=['pandas==0.22.0', 'numpy==1.14.2'],
    author="Vikram Tiwari",
    author_email="vikramtheone1@gmail.com",
    description=("Custom python utils needed for dataflow cloud runner"),
    packages=find_packages(),
    package_data={"Common": [".credentials/*.json"]},
    include_package_data=True)
