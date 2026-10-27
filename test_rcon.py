from pathlib import Path
from mcrcon import MCRcon

password_file = (
    Path.home()
    / ".config/minecraft-lab/rcon_password"
)

password = password_file.read_text().strip()

with MCRcon("127.0.0.1", password, port=25575) as client:
    response = client.command("list")
    print(response)
