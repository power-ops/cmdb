import zipfile
from os import listdir
from os.path import isfile, join


def unzip(filename):
    z = zipfile.ZipFile(filename)
    z.extractall()
    z.close()


def find_zip(dir):
    return [f for f in listdir(dir) if isfile(join(dir, f)) and ".zip" in f]
