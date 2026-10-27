from pathlib import Path
from mcrcon import MCRcon

password = (
    Path.home() / ".config/minecraft-lab/rcon_password"
).read_text().strip()

x, z = 14, 11

blocks = [
    "grass_block",
    "dirt",
    "stone",
    "sand",
    "gravel",
    "bedrock",
    "cobblestone",
    "air",
    "water",
]

with MCRcon("127.0.0.1", password, port=25575) as mc:
    for y in range(58, 66):
        for block in blocks:
            command = (
                f"execute if block {x} {y} {z} "
                f"minecraft:{block}"
            )
            result = mc.command(command)

            if "Test passed" in result:
                print(f"Found minecraft:{block} at Y={y}")
