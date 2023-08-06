import os

def progress_int_read(progress_path, default=-1):
    if not os.path.exists(progress_path):
        return default
    return int(open(progress_path, 'r').read())

def progress_int_write(progress_path, value_int):
    with open(progress_path, 'w', encoding='utf-8') as f:
        f.write("{}".format(value_int))