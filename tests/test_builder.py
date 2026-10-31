
import unittest
from unittest.mock import patch

from builder import build_gate, build_wall


class FakeMinecraftRcon:
    """Fake RCON client: records commands without connecting to Minecraft."""

    def __init__(self):
        self.commands = []

    def get_player_position(self, player):
        return 0.0, 64.0, 0.0

    def get_player_rotation(self, player):
        return 0.0, 0.0

    def command(self, command):
        self.commands.append(command)

        if command.startswith("setblock"):
            return "Block placed"
        if command.startswith("fill"):
            return "Successfully filled 5 blocks"

        return "Unknown command"


def gate_settings():
    return {
        "name": "test_gate",
        "width": 12,
        "height": 5,
        "opening_width": 4,
        "opening_height": 4,
        "distance": 3,
        "search_above": 6,
        "search_below": 20,
        "block": "minecraft:stone",
    }


class TestBuildGate(unittest.TestCase):

    def setUp(self):
        self.mc = FakeMinecraftRcon()

    @patch("builder.find_ground", return_value=63)
    def test_gate_builds_sides_and_lintel(self, find_ground_mock):
        result = build_gate(self.mc, gate_settings())

        self.assertEqual(result, 0)
        self.assertEqual(len(self.mc.commands), 12)

        fill_commands = [
            command for command in self.mc.commands
            if command.startswith("fill ")
        ]
        setblock_commands = [
            command for command in self.mc.commands
            if command.startswith("setblock ")
        ]

        # Eight side columns are full height.
        self.assertEqual(len(fill_commands), 8)

        # Four opening columns receive only the lintel block.
        self.assertEqual(len(setblock_commands), 4)

        # Ground is checked independently for every column.
        self.assertEqual(find_ground_mock.call_count, 12)

        for command in setblock_commands:
            parts = command.split()
            self.assertEqual(parts[2], "68")
            self.assertEqual(parts[4], "minecraft:stone")

        for command in fill_commands:
            parts = command.split()
            self.assertEqual(parts[2], "64")
            self.assertEqual(parts[5], "68")
            self.assertEqual(parts[7], "minecraft:stone")

    @patch("builder.find_ground", return_value=None)
    def test_gate_returns_error_when_ground_is_missing(
        self, find_ground_mock
    ):
        result = build_gate(self.mc, gate_settings())

        self.assertEqual(result, 1)
        self.assertEqual(self.mc.commands, [])
        self.assertEqual(find_ground_mock.call_count, 12)

    @patch("builder.find_ground", return_value=63)
    def test_gate_command_failure_returns_error(self, find_ground_mock):
        self.mc.command = lambda command: "Command failed"

        result = build_gate(self.mc, gate_settings())

        self.assertEqual(result, 1)


class TestBuildWall(unittest.TestCase):

    @patch("builder.find_ground", return_value=63)
    def test_wall_still_builds_full_height_columns(
        self, find_ground_mock
    ):
        mc = FakeMinecraftRcon()
        settings = gate_settings()

        result = build_wall(mc, settings)

        self.assertEqual(result, 0)
        self.assertEqual(len(mc.commands), 12)
        self.assertTrue(
            all(command.startswith("fill ") for command in mc.commands)
        )
        self.assertEqual(find_ground_mock.call_count, 12)


if __name__ == "__main__":
    unittest.main()
