
import re
from pathlib import Path

from mcrcon import MCRcon


RCON_HOST = "127.0.0.1"
RCON_PORT = 25575

PASSWORD_FILE = (
    Path.home() / ".config/minecraft-lab/rcon_password"
)


class MinecraftRcon:
    """Connection to a Minecraft server through RCON."""

    def __init__(self, host=RCON_HOST, port=RCON_PORT):
        self.host = host
        self.port = port
        self._connection = None

    def __enter__(self):
        password = PASSWORD_FILE.read_text().strip()

        if not password:
            raise ValueError("RCON password file is empty")

        self._connection = MCRcon(
            self.host,
            password,
            port=self.port,
        )
        self._connection.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._connection is not None:
            self._connection.disconnect()
            self._connection = None

    def command(self, command):
        """Execute a command and return the server response."""
        if self._connection is None:
            raise RuntimeError("RCON is not connected")

        return self._connection.command(command)

    def get_player_position(self, player):
        """Return player coordinates as floats: (x, y, z)."""
        response = self.command(
            f"data get entity {player} Pos"
        )

        match = re.search(
            r"\[([-0-9.eE]+)d?,\s*"
            r"([-0-9.eE]+)d?,\s*"
            r"([-0-9.eE]+)d?\]",
            response,
        )

        if not match:
            raise RuntimeError(
                f"Could not read position for {player}: "
                f"{response}"
            )

        return tuple(map(float, match.groups()))

    def get_player_rotation(self, player):
        """Return player yaw and pitch as floats."""
        response = self.command(
            f"data get entity {player} Rotation"
        )

        match = re.search(
            r"\[([-0-9.eE]+)f?,\s*"
            r"([-0-9.eE]+)f?\]",
            response,
        )

        if not match:
            raise RuntimeError(
                f"Could not read rotation for {player}: "
                f"{response}"
            )

        return tuple(map(float, match.groups()))

