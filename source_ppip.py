import requests
import sys
import os
import tarfile
import zipfile
import shutil
import pprint


path = "/Users/svs/pypy3-v6.0.0-osx64/site-packages/"


def move_path(src, des):
    for i in os.walk(src):
        if os.path.isdir(src + "/" + i):
            try:
                os.mkdir(src + "/" + i)
            except FileExistsError:
                pass
            move_path(src + "/" + i, des + "/" + i)
        else:
            shutil.move(src + "/" + i, des + "/" + i)


def install(package):
    inst.append(package)
    desc = requests.get("https://pypi.org/pypi/" + package + "/json")
    if not desc:
        return
    desc = desc.json()
    print ("Installing package " + package + ".")
    print("Installing dependencies...")
    if not (desc['info']['requires_dist'] is None):
        dependencies = desc['info']['requires_dist']
        for m in dependencies:
            i = m.split(";")[0].split(" ")[0]
            if not (i in inst) and not ("dev" in m or "docs" in m):
                install(i)
    print("Searching for the latest version...")
    version = list(desc["releases"].keys())[-1]
    print("Downloading archive...")
    download = list(filter(
        lambda x: x["python_version"] == "source",
        desc["releases"][version]))[0]
    link = download["url"]
    filename = link.split("/")[-1]
    archive_path = os.path.join(path, filename)
    with open(archive_path, "wb") as archive:
        archive.write(requests.get(link).content)
        new_path = ".".join(archive_path.split(".")[:-1]) + ".zip"
        os.rename(archive_path, new_path)
        archive_path = new_path
    print("Extracting...")
    with tarfile.open(archive_path, 'r') as archive:
        archive.extractall(path=path + package.lower())
    print("Removing unneeded items...")
    os.remove(archive_path)
    print("Moving items...")
    archive_path = path + package.lower()
    for x in os.listdir(archive_path):
        for item in os.listdir (archive_path + "/" + x):
            shutil.move(archive_path + "/" + x + "/" + item, archive_path)
    print("Running setup.py...")
    setup_path = archive_path + "/setup.py"
    os.system("python " + setup_path + " build")
    os.system("python " + setup_path + " install")
    print("Moving the results...")
    other = os.listdir(archive_path)
    build_path = archive_path + "/build"
    for x in os.listdir(build_path):
        if x.split(".")[0] == "lib":
            src_path = build_path + "/" + x + "/" + package.lower()
            des_path = path + package.lower()
            move_path(src_path, des_path)
    print("Done!")


if __name__ == "__main__":
    name = None
    try:
        name = sys.argv[1]
    except IndexError:
        name = input("Name of the package: ")
    file = open("installed.txt", "r")
    inst = file.read().split("\n")
    file.close()
    install(name)
    file = open ("installed.txt", "w")
    file.write("\n".join(inst))
    file.close()
