#!/usr/bin/python
#coding = utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="windget", # Replace with your own username
    version="0.0.6",
    author="Syuya_Murakami",
    author_email="wxy135@mail.ustc.edu.cn",
    description="windget a is third party Win.D API for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.baidu.com",
    project_urls={
        "Bug Tracker": "https://www.baidu.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
        ]
    }
)
