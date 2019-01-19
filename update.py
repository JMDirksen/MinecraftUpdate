import urllib.request
import json
import os

# release or snapshot
TYPE = "release"

def main():
    version = get_latest_version(TYPE)
    filename = "minecraft_server.%s.jar" % version["id"]
    print(version["filename"])
    print(file_exists(version["filename"]))
    print(version["download_url"])
    

def get_latest_version(type):
    manifest_url = \
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest_json_file = urllib.request.urlopen(manifest_url)
    manifest = json.load(manifest_json_file)
    latest_version_id = manifest["latest"][type]
    for latest_version in manifest["versions"]:
        if latest_version["id"] == latest_version_id:
            break
    
    version_url = latest_version["url"]
    version_json_file = urllib.request.urlopen(version_url)
    version = json.load(version_json_file)
    
    return {
        "id": version["id"],
        "filename": "minecraft_server.%s.jar" % version["id"],
        "download_url": version["downloads"]["server"]["url"],
        }

def file_exists(filepath):
    return os.path.isfile(filepath)

main()
