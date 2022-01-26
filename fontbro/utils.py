# -*- coding: utf-8 -*-

import fsutil


def read_json(filepath):
    return fsutil.read_file_json(fsutil.join_path(__file__, filepath))


def slugify(s):
    return s.lower().replace(" ", "-")
