import fsutil
from fontTools import unicodedata

from fontbro import Font


def _write_data_json(filepath, data):
    data_filepath = fsutil.join_path(__file__, filepath)
    fsutil.write_file_json(data_filepath, data, indent=4, sort_keys=True)


def update_unicode_data():
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

    _write_data_json(filepath="../fontbro/data/unicode-blocks.json", data=blocks)
    _write_data_json(filepath="../fontbro/data/unicode-scripts.json", data=scripts)


def main():
    update_unicode_data()


if __name__ == "__main__":
    main()
