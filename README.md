# MinecraftUpdate
Python script for downloading and updating Mincraft server to latest version.

## Setup
- Download or clone this repository
- Copy config.example.json to config.json
- Edit the config.json as necessary
    - `type`: The version type to update to, can either be 'release' or 'snapshot'
    - `server_path`: The (relative) path to the Minecraft server files (server.jar)
    - `rcon_host`: The hostname or ip of the Minecraft server for RCON connection (RCON is used to gracefully stop the Minecraft server when updating)
    - `rcon_port`: The port RCON is running on (see Minecraft server.properties)
    - `rcon_password`: The password for the RCON connection (see Minecraft server.properties)
    - `start_command`: The command to start de Minecraft server again after update
