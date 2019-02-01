import os
import urllib.request
import json
from MCRcon.mcrcon import MCRcon
from shutil import copyfile

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)


def main():
    version = get_latest_version(config["type"])
    if file_exists(version["filename"]):
        print("No new version")
        os._exit(0)
    print("Downloading new version...")
    download(version["download_url"], version["filename"])
    stop_server(config["rcon_host"], config["rcon_port"], config["rcon_password"])
    try:
        copyfile(version["filename"], config["server_path"] + "server.jar")
        print("Update completed.")
    except FileNotFoundError:
        print("Unable to update server, is your config (server_path) correct?")


def get_latest_version(type):
    """Get information about the latest version from Mojang."""
    manifest_url = \
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest = url_to_obj(manifest_url)
    for latest_version in manifest["versions"]:
        if latest_version["id"] == manifest["latest"][type]:
            break
    version = url_to_obj(latest_version["url"])

    return {
        "id": version["id"],
        "filename": "minecraft_server.%s.jar" % version["id"],
        "download_url": version["downloads"]["server"]["url"],
    }


def url_to_obj(json_url):
    """Download the json and convert it to an object."""
    return json.load(urllib.request.urlopen(json_url))


def download(url, filename):
    """Download a file and store it as filename."""
    urllib.request.urlretrieve(url, filename)


def file_exists(filepath):
    """Test if the file exists."""
    return os.path.isfile(filepath)


def stop_server(host, rcon_port, rcon_password):
    try:
        rcon = MCRcon()
        rcon.connect(host, rcon_port, rcon_password)
        rcon.command("stop")
    except ConnectionRefusedError:
        print("Failed to stop server, maybe it's not running? Or your config may be incorrect.")


main()
