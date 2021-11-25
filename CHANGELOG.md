# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.2.2) - 2021-11-25
-   Fixed `rename` method to raise a `ValueError` when the computed PostScript name exceeds the allowed max-length (63).
-   Fixed `to_sliced_variable` when axes coordinates are passed as dict doesn't contain 'min' or 'max' keys.
-   Changed `get_variable_axes` and `get_variable_instances` returned dicts keys from camelCase to snake_keys.
-   Changed `get_variable_instances` method return value.
-   Reduced return calls in `get_format` method.
-   Improved tests.

## [0.2.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.2.1) - 2021-11-19
-   Fixed width axis tag name.

## [0.2.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.2.0) - 2021-11-19
-   Added `get_features_tags` method.
-   Added `get_style_flag` and `set_style_flag` methods.
-   Added support to `'condensed'`, `'extended'` and `'shadow'` style flags.
-   Added `rename` method.

## [0.1.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.1.0) - 2021-11-18
-   Released `python-fontbro`.
