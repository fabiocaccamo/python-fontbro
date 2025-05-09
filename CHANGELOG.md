# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.24.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.24.0) - 2024-08-05
-   Add `get_svg` method.
-   Add `is_color` method.
-   Improve `is_monospace` method accuracy by adding `threshold` option.
-   Bump requirements.

## [0.23.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.23.1) - 2024-07-08
-   Fix `get_format` with `.otf` fonts with `CFF2` table.
-   Bump requirements and `pre-commit` hooks

## [0.23.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.23.0) - 2024-06-23
-   Add `get_family_classification` and `set_family_classification` methods.
-   Improve `slugify` utility function.
-   Bump requirements and `pre-commit` hooks

## [0.22.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.22.0) - 2024-05-14
-   Add `is_monospace` method.
-   Add `mypy` to `pre-commit`.
-   Fix `pyproject` `Ruff` conf warnings.
-   Bump requirements and `pre-commit` hooks

## [0.21.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.21.0) - 2024-03-07
-   Add type hints.
-   Add vertical metrics keys available as class properties.
-   Improve code quality.
-   Bump requirements and `pre-commit` hooks

## [0.20.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.20.0) - 2024-01-29
-   Add more vertical metrics: `units_per_em`, `y_max`, `y_min`, `ascent`, `descent`, `line_gap`, `typo_ascender`, `typo_descender`, `typo_line_gap`, `cap_height`, `x_height`, `win_ascent`, `win_descent`.

## [0.19.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.19.0) - 2024-01-28
-   Add `get_vertical_metrics` and `set_vertical_metrics` methods. (#150)

## [0.18.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.18.0) - 2024-01-06
-   Add `sanitize` method.
-   Enforce keyword arguments usage.
-   Use custom exceptions.

## [0.17.2](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.17.2) - 2023-12-18
-   Fix possible `TypeError`: '<' not supported between instances of 'NoneType' and 'int'.

## [0.17.1](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.17.1) - 2023-12-18
-   Add `get_variable_instance_by_style_name` method.
-   Increase tests coverage.

## [0.17.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.17.0) - 2023-12-13
-   Add `Python 3.12` support.
-   Add `get_family_name` / `set_family_name` methods.
-   Add `get_filename` method.
-   Add `get_style_name` / `set_style_name` methods.
-   Add `save_variable_instances` method. #116
-   Update `rename` method: rename `style_flags` argument to `update_style_flags`.
-   Update `save` method: output font filename is generated using `get_filename` method when target path is a directory.
-   Update `to_static` method: add support to `update_names` (default True) and `update_style_flags` (default True) arguments.
-   Update `to_static` method: set `italic` style flag based on `ital` / `slnt` coordinates values.
-   Fix `get_variable_instance_closest_to_coordinates`: if coordinates do not specify some axes, axes default value is used for lookup.
-   Fix `to_static` method: prevent `inplace` option override.
-   Use `Ruff` formatter instead of `Black` and `isort`.
-   Bump requirements (`fonttools`, `pillow` and `python-fsutil`).

## [0.16.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.16.0) - 2023-09-19
-   Add `Font.from_collection` class method. #49
-   Allow initialisation from `fontbro.Font` / `fontTools.ttLib.TTFont` objects.
-   Fix error when calling `clone` method on a `Font` object created using a fileobject. #118
-   Bump requirements.

## [0.15.0](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.15.0) - 2023-08-28
-   Allow instantiation with file objects. (by [@fcurella](https://github.com/fcurella) in #103)
-   Add `save_to_file_object` method. (by [@fcurella](https://github.com/fcurella) in #103)
-   Bump requirements (`fonttools`, `coverage`, `pre-commit` and `tox`).

## [0.14.15](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.15) - 2023-07-31
-   Bump requirements (`fonttools`, `pillow` and `tox`).

## [0.14.14](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.14) - 2023-06-05
-   Allow `filepath` of type `pathib.Path` in constructor. #83 (#84)
-   Add possibility to create static instance by using `style_name` instead of `coordinates`. #82 (#85)
-   Strip whitespace when `slugify` string.
-   Move `get_euclidean_distance` function to `fontbro.math` module.
-   Bump `fonttools[pathops,unicode,woff]` from `4.39.3` to `4.39.4`. (#79)
-   Update `pre-commit` hooks. (#80)

## [0.14.13](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.13) - 2023-05-02
-   Fix `Font Bakery` error: "Verify that each group of fonts with the same nameID 1 has maximum of 4 fonts".

## [0.14.12](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.12) - 2023-05-02
-   Fix `Font Bakery` error: "font name does not begin with the font family name".

## [0.14.11](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.11) - 2023-05-02
-   Fix renaming legacy name records 1 and 2.

## [0.14.10](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.10) - 2023-04-24
-   Revert "Fix `family_name` name record renaming."

## [0.14.9](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.9) - 2023-04-18
-   Calculate Euclidean distance between dicts.

## [0.14.8](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.8) - 2023-04-17
-   Fix `family_name` renaming.
-   Fix `tox` test command.
-   Replace `flake8` with `Ruff`.
-   Switch from `setup.cfg` to `pyproject.toml`.
-   Bump `fonttools[pathops,unicode,woff]` from `4.39.2` to `4.39.3`. (#68)
-   Bump `pillow` from `9.4.0` to `9.5.0`. (#71)

## [0.14.7](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.7) - 2023-03-24
-   Improve `full_name` renaming using name records IDs 16 and 17. #62 (#66)

## [0.14.6](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.6) - 2023-03-21
-   Accept axis coordinates `dict` with `default` in `to_sliced_variable` method. #63
-   Update unique identifier name record when renaming font. #62
-   Upgrade syntax for `Python >= 3.8`.
-   Set max line length to `88`.
-   Add `flake8-bugbear` to `pre-commit`.
-   Run `flake8` also on tests files.
-   Bump requirements.

## [0.14.5](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.5) - 2023-01-29
-   Fix `get_image()` crash on Windows. (by [@seproDev](https://github.com/seproDev) in #53)
-   Correctly center text in `get_image()`. (by [@seproDev](https://github.com/seproDev) in #53)
-   Fix `AttributeError` in `get_features()`. #50 (by [@seproDev](https://github.com/seproDev) in #53)
-   Set `unicode_name` default to `None`. #51 (by [@seproDev](https://github.com/seproDev) in #53)

## [0.14.4](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.4) - 2023-01-12
-   Automatically update unicode data once a month.
-   Update `unicode-blocks.json` and `unicode-scripts.json` data.
-   Fix unformatted string in `get_characters` method.

## [0.14.3](https://github.com/fabiocaccamo/python-fontbro/releases/tag/0.14.3) - 2023-01-12
-   Bump `python-fsutil` requirement.

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
