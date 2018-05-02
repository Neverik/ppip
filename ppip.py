import requests
import sys
import os
import tarfile
import zipfile
import shutil
import pprint


path = "/Users/svs/pypy3-v6.0.0-osx64/site-packages/"


def install(package):
    os.system("pip install --target=" + path + " " + package)


if __name__ == "__main__":
    name = None
    try:
        name = sys.argv[1]
    except IndexError:
        name = input("Name of the package: ")
    install(name)
