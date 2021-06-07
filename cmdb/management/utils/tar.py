import tarfile

from os import listdir
from os.path import isfile, join


def untar(tar_path, target_path):
    tar = tarfile.open(tar_path, "r:gz")
    file_names = tar.getnames()
    for file_name in file_names:
        tar.extract(file_name, target_path)
    tar.close()

def find_tar_gz(dir):
    return [f for f in listdir(dir) if isfile(join(dir, f)) and ".tar.gz" in f]

