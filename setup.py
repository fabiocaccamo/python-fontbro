#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import os

exec(open("fontbro/metadata.py").read())

github_url = "https://github.com/fabiocaccamo"
sponsor_url = "https://github.com/sponsors/fabiocaccamo/"
twitter_url = "https://twitter.com/fabiocaccamo"
package_name = "python-fontbro"
package_url = "{}/{}".format(github_url, package_name)
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, "README.md")
long_description_content_type = "text/markdown"
long_description = ""
try:
    with open(long_description_file_path, "r", encoding="utf-8") as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author=__author__,
    author_email=__email__,
    url=package_url,
    download_url="{}/archive/{}.tar.gz".format(package_url, __version__),
    project_urls={
        "Documentation": "{}#readme".format(package_url),
        "Issues": "{}/issues".format(package_url),
        "Funding": sponsor_url,
        "Twitter": twitter_url,
    },
    keywords=[
        "font",
        "fonttools",
        "languages",
        "opentype",
        "otf",
        "python",
        "scripts",
        "slicing",
        "subset",
        "subsetting ",
        "ttf",
        "unicode",
        "utility",
        "variable",
        "variations",
        "woff",
        "woff2",
        "wrapper",
        "writing-systems",
    ],
    install_requires=[
        # 'fonttools[ufo,lxml,woff,unicode,interpolatable,plot,symfont,type1,pathops] >= 4.27.0, < 5.0',
        "fonttools[woff,unicode,pathops] >= 4.27.0, < 5.0",
        "imagehash >= 4.2.1, < 5.0.0",
        "pillow >= 8.4.0, < 10.0.0",
        "python-fsutil >= 0.6.0, < 1.0.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Text Processing :: Fonts",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    license=__license__,
    test_suite="tests",
)
