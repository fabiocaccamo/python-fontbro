[![](https://img.shields.io/pypi/pyversions/python-fontbro.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-fontbro.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-fontbro/)
[![](https://pepy.tech/badge/python-fontbro)](https://pepy.tech/project/python-fontbro)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-fontbro?logo=github)](https://github.com/fabiocaccamo/python-fontbro/)
[![](https://badges.pufler.dev/visits/fabiocaccamo/python-fontbro?label=visitors&color=blue)](https://badges.pufler.dev)
[![](https://img.shields.io/pypi/l/python-fontbro.svg?color=blue)](https://github.com/fabiocaccamo/python-fontbro/blob/master/LICENSE.txt)

[![](https://img.shields.io/travis/fabiocaccamo/python-fontbro?logo=travis&label=build)](https://travis-ci.org/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/circleci/build/gh/fabiocaccamo/python-fontbro?logo=circleci&label=build)](https://circleci.com/gh/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-fontbro?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/codacy/grade/fc40788ae7d74d1fb34a38934113c4e5?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-fontbro)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/python-fontbro?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-fontbro/)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# python-fontbro
human-friendly font operations on top of `fontTools`. :tumbler_glass:

## Features
-   ...

## Index
-   [Installation](#installation)
-   [Usage](#usage)
-   [Testing](#testing)
-   [License](#license)

## Installation

```bash
pip install python-fontbro
```

## Usage

### Methods

## Testing
```bash
# create python virtual environment
virtualenv testing_fontbro

# activate virtualenv
cd testing_fontbro && . bin/activate

# clone repo
git clone https://github.com/fabiocaccamo/python-fontbro.git src && cd src

# install requirements
pip install --upgrade pip
pip install -r requirements.txt

# run tests using tox
tox

# or run tests using unittest
python -m unittest

# or run tests using setuptools
python setup.py test
```

## License
Released under [MIT License](LICENSE.txt).

---

## See also

- [`python-benedict`](https://github.com/fabiocaccamo/python-benedict) - dict subclass with keylist/keypath support, I/O shortcuts (base64, csv, json, pickle, plist, query-string, toml, xml, yaml) and many utilities. 📘
- [`python-fsutil`](https://github.com/fabiocaccamo/python-fsutil) - file-system utilities for lazy devs. 🧟‍♂️
