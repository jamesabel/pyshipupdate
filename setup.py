from setuptools import setup

from pyshipupdate import __application_name__, __author__, __version__, __description__, __author_email__, __download_url__, __url__

requirements = ["balsa", "requests", "attrs", "typeguard", "semver", "python-dateutil", "boto3", "awsimple", "pywin32"]

with open("readme.md", encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name=__application_name__,
    version=__version__,
    author=__author__,
    install_requires=requirements,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email=__author_email__,
    license="MIT License",
    url=__url__,
    download_url=__download_url__,
    keywords=["freezer", "installer", "ship"],
    classifiers=[],
    packages=[__application_name__],
    package_data={
        "": ["*.ico"],
    },
)
