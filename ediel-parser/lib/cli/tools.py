import os

def get_files(path, blacklist=True):
    filenames = os.listdir(path)
    if blacklist is True:
        filenames = filter(lambda f: f.lower() not in ['.ds_store'], filenames)
    full_paths = map(lambda f: os.path.join(path, f), filenames)
    files = filter(os.path.isfile, full_paths)
    return list(files)
    # cleaned = map(lambda x: x.replace('.mail', ''), filenames)
    # return list(filter(lambda f: f.isdigit(), cleaned))