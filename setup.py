#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import os, sys

exec(open('fontbro/metadata.py').read())

github_url = 'https://github.com/fabiocaccamo'
package_name = 'python-fontbro'
package_url = '{}/{}'.format(github_url, package_name)
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, 'README.md')
long_description_content_type = 'text/markdown'
long_description = ''
try:
    long_description_file_options = (
        {} if sys.version_info[0] < 3 else {'encoding': 'utf-8'}
    )
    with open(long_description_file_path, 'r', **long_description_file_options) as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author=__author__,
    author_email=__email__,
    url=package_url,
    download_url='{}/archive/{}.tar.gz'.format(package_url, __version__),
    keywords=[
        'font',
        'fonttools',
        'languages',
        'opentype',
        'otf',
        'python',
        'scripts',
        'slicing',
        'subset',
        'subsetting ',
        'ttf',
        'unicode',
        'utility',
        'variable',
        'variations',
        'woff',
        'woff2',
        'wrapper',
        'writing-systems',
    ],
    install_requires=[
        # 'fonttools[ufo,lxml,woff,unicode,interpolatable,plot,symfont,type1,pathops] >= 4.27.0, < 5.0',
        'fonttools[woff,unicode,pathops] >= 4.27.0, < 5.0',
        'python-fsutil >= 0.5.0, < 1.0.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    ],
    license=__license__,
    test_suite='tests',
)
