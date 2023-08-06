"""
Setup auto_utils
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = [
    'autoutils',
    'matrixcli'
]

install_requires = [
    "persiantools>=2.0",
    "redis>=4.0",
    "requests>=2.0",
    "urllib3>=1.0",
    "sshtunnel>=0.1",
    "paramiko>=2.0",
    "func-timeout>=4.0",
    "blessings>=1.0"
]

setup(
    name="autoutils",
    version="0.1.1",
    author="Reza Zeiny",
    author_email="rezazeiny1998@gmail.com",
    description="Some Good Function",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rezazeiny/autoutils",
    packages=packages,
    platforms=['linux'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
