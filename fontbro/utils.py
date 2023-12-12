import fsutil


def concat_names(a, b):
    return f"{a} {b}" if not a.endswith(f" {b}") else a


def read_json(filepath):
    return fsutil.read_file_json(fsutil.join_path(__file__, filepath))


def remove_spaces(s):
    return s.replace(" ", "")


def slugify(s):
    return s.lower().strip().replace(" ", "-")
