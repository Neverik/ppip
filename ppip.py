import requests
import sys
import wget
import os
import zipfile


path = "/Users/svs/pypy3-v6.0.0-osx64/site-packages/"


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
        lambda x: ('3' in x["python_version"]) and (not ("win" in x["filename"])),
        desc["releases"][version]))[0]
    link = download["url"]
    filename = link.split("/")[-1]
    assert filename.split(".")[-1] == "whl"
    wheel_path = os.path.join(path, filename)
    with open(wheel_path, "wb") as wheel:
        wheel.write(requests.get(link).content)
        new_path = ".".join(wheel_path.split(".")[:-1]) + ".zip"
        os.rename(wheel_path, new_path)
        wheel_path = new_path
    print("Extracting...")
    with zipfile.ZipFile(wheel_path, 'r') as wheel:
        wheel.extractall("/".join(wheel_path.split("/")[:-1]))
    print("Removing unneeded items...")
    os.remove(wheel_path)
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
