# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.14.2](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.2) - 2023-01-11
-   Add `ignore_blank` option to `get_characters` and `get_characters_count` methods.
-   Fix `Pillow` `textsize` method deprecation warning.
-   Bump requirements.

## [0.14.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.1) - 2023-01-03
-   Update unicode data.

## [0.14.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.0) - 2023-01-03
-   Drop `Python 3.7` support.
-   Add `setup.cfg` (`setuptools` declarative syntax) generated using `setuptools-py2cfg`.
-   Add `pyupgrade` to `pre-commit` config.
-   Bump requirements and actions.
-   Pin test requirements.

## [0.13.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.13.0) - 2022-12-14
-   Add `Python 3.11` support.
-   Replace `str.format` with `f-strings`.
-   Remove encoding pragma.
-   Remove `python setup.py test` usage.
-   Bump requirements and actions.

## [0.12.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.12.0) - 2022-10-21
-   Add `pre-commit`.
-   Add `get_glyphs` and `get_glyphs_count` methods.
-   Fix PostScript name allowed characters (keep only printable ASCII subset).

## [0.11.2](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.11.2) - 2022-09-19
-   Add `lazy` option support to constructor.
-   Fix subfamily name (name ID 2) renaming (lower case -> title case).
-   Fix Pillow deprecation warning.
-   Update requirements.

## [0.11.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.11.1) - 2022-07-05
-   Updated `rename` for generating the `full_name` combining `family_name` and `subfamily_name`.

## [0.11.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.11.0) - 2022-06-30
-   Added `set_style_flags_by_subfamily_name` method.
-   Added `style_flags=True` option to `rename` method.
-   Updated `get_features_tags` method for checking also the `GPOS` table.

## [0.10.4](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.10.4) - 2022-06-29
-   Improved renaming according to RIBBI.

## [0.10.3](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.10.3) - 2022-06-29
-   Fixed `rename` subfamily name when there are `Regular` and `Italic` in the same name.

## [0.10.2](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.10.2) - 2022-06-28
-   Fixed style flags on save according to subfamily name.

## [0.10.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.10.1) - 2022-06-28
-   Improved renaming according to RIBBI.
-   Fixed `rename` subfamily name error.

## [0.10.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.10.0) - 2022-06-28
-   Improved renaming according to RIBBI.
-   Updated style flags on save according to subfamily name.

## [0.9.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.9.1) - 2022-06-07
-   Updated `subset` default options.

## [0.9.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.9.0) - 2022-06-07
-   Added possibility to pass subsetter options via kwargs in `subset` method.
-   Updated docstrings.

## [0.8.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.8.0) - 2022-05-08
-   Added `clone` method.
-   Added `get_fingerprint_match` method.
-   Added `get_version` method.
-   Removed `match` method.

## [0.7.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.7.0) - 2022-04-29
-   Added `get_fingerprint` method.
-   Added `get_image` method.
-   Added `get_italic_angle` method.
-   Added `match` method.
-   Refactored `get_weight` and `get_width` methods.
-   Updated unicode blocks and scripts data.
-   Updated requirements.

## [0.6.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.6.0) - 2022-02-21
-   Added `close` method.
-   Added possibility to use `Font` class as context manager.

## [0.5.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.5.0) - 2022-01-26
-   Improved `subset` `unicodes` arg to support also list of `int` codepoints.
-   Moved features and unicode data to json files.
-   Moved `parse_unicodes` to the subset module and made it a public re-usable function.
-   Updated `python-fsutil` requirement version to `0.6.0`.

## [0.4.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.4.0) - 2022-01-12
-   Added more informations to characters returned by `get_characters` method.
-   Added `get_unicode_block_by_name` and `get_unicode_script_by_name` methods.
-   Improved `subset` unicodes parsing.
-   Renamed `uni` module to `unicodedata`.

## [0.3.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.3.0) - 2022-01-11
-   Added `get_unicode_blocks` method.
-   Added `get_unicode_scripts` method.
-   Changed `get_name` and `set_name` to read/write both Mac and Windows IDs.
-   Fixed hardcoded class name in `__str__` method.
-   Fixed `setup.py` warning and updated to `tox` configuration.
-   Removed `get_scripts` method.
-   Removed `get_scripts_by_characters` class method.
-   Replaced single quotes `'` with double quotes `"` (**Black** formatting).

## [0.2.3](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.2.3) - 2021-12-09
-   Added `get_scripts_by_characters` class method.
-   Fixed `TypeError` raised on save after renaming.
-   Fixed `get_name` and `set_name` langID parameter.
-   Improved `subset` unicodes string parsing.
-   Replaced **Travis CI** with **Github Workflow**.
-   Formatted code with **Black**.

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
