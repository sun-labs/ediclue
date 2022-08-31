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

def filter_blacklist(file):
    blacklist = ['.DS_Store']
    return file not in blacklist

def map_with_path(path):
    return lambda f: os.path.join(path, f)

def extract_filename(full_path):
    return full_path.split('/')[-1]

def get_files(path, cb=None, *, mode='r'):
    filenames = os.listdir(path)
    filenames = list(filter(filter_blacklist, filenames))
    full_paths = list(map(map_with_path(path), filenames))
    full_paths = list(filter(os.path.isfile, full_paths))
    filenames = list(map(extract_filename, full_paths))
    return filenames, full_paths

# map files and open with file handler
def map_files(full_paths: [str], cb=None, *, mode='r'):
    if cb is not None:
        for path in full_paths:
            fh = open(path, mode)
            cb(fh, path, extract_filename(path))
            fh.close()

def extension_for_type(file_type):
    ft = file_type
    if ft == 'mail':
        return 'eml'
    else:
        return file_type