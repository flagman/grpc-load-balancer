from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="grpc_load_balancer",
    version="0.0.1",
    author="Pavel Malay",
    author_email="flagmansupport@gmail.com",
    description="A small toolset to implement load balancing for gRPC services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flagman/grpc-load-balancer",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
