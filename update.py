import os
import urllib.request
import json
import time
from mcrcon import MCRcon
from shutil import copyfile
from datetime import datetime

# Load config
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    output("Missing config.json, please copy config.example.json to config.json and modify as needed.")
    os._exit(1)

def main():
    version = get_latest_version(config["type"])
    if file_exists(version["filename"]):
        output("No new version")
        time.sleep(3)
        os._exit(0)
    output("Downloading new version...")
    download(version["download_url"], version["filename"])
    output("Stopping server...")
    stop_server(config["rcon_host"], config["rcon_port"], config["rcon_password"])
    try:
        copyfile(version["filename"], config["server_path"] + "server.jar")
        output("Update completed.")
    except FileNotFoundError:
        output("Unable to update server, is your config (server_path) correct?")
    start_server()
    output("Done.")
    time.sleep(3)


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
        with MCRcon(host, rcon_password, rcon_port) as mcr:
            mcr.command("stop")
        time.sleep(10)
    except ConnectionRefusedError:
        output("Failed to stop server, maybe it's not running? Or your config may be incorrect.")


def start_server():
    output("Starting server...")
    os.system(config["start_command"])


def output(message):
    print(message)
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    with open("update.log", "a") as f:
        f.write(dt_string + message + "\n")

main()
