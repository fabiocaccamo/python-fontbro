# -*- coding: utf-8 -*-

import json

import fsutil
from fontTools import unicodedata

from fontbro import Font
from tests import AbstractTestCase


class UpdateUnicodeDataTestCase(AbstractTestCase):
    """
    Test case for updating the pre-computed unicode data.
    """

    def test_update_unicode_data(self):
        blocks = []
        blocks_cache = {}
        scripts = []
        scripts_cache = {}
        for code in range(0, 0x110000):
            block_name = unicodedata.block(code)
            if block_name == "No_Block":
                continue
            block = {
                "name": block_name,
            }
            Font._populate_unicode_items_set(blocks, blocks_cache, block)
            script_tag = unicodedata.script(code)
            script_name = unicodedata.script_name(script_tag)
            script = {
                "name": script_name,
                "tag": script_tag,
            }
            Font._populate_unicode_items_set(scripts, scripts_cache, script)

        for block in blocks:
            block["characters_total"] = block["characters_count"]
            block.pop("characters_count", None)

        for script in scripts:
            script["characters_total"] = script["characters_count"]
            script.pop("characters_count", None)

        data_dir = fsutil.join_path(__file__, "../fontbro/data/")
        fsutil.write_file(
            fsutil.join_path(data_dir, "unicode-blocks.json"),
            json.dumps(blocks, sort_keys=True, indent=4),
        )
        fsutil.write_file(
            fsutil.join_path(data_dir, "unicode-scripts.json"),
            json.dumps(scripts, sort_keys=True, indent=4),
        )
