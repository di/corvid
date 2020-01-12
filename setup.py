from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="corvid",
    version="1.0.0",
    description="An opinionated simple static site generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/di/corvid",
    author="Dustin Ingram",
    author_email="di@python.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="static markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.5, <4",
    install_requires=[
        "click>=7.0<=8.0",
        "python-frontmatter>=0.5.0",
        "Markdown>=3.1",
        "jinja2>=2.10",
        "watchdog>=0.9.0",
    ],
    extras_require={"test": ["pytest", "tox"]},
    entry_points={"console_scripts": ["corvid=corvid:cli"]},
)
