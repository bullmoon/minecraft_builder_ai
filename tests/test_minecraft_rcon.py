
import unittest
from unittest.mock import Mock, patch

from minecraft_rcon import MinecraftRcon


class TestMinecraftRcon(unittest.TestCase):

    def setUp(self):
        self.password_file = patch(
            "minecraft_rcon.PASSWORD_FILE"
        )
        self.mock_password_file = self.password_file.start()
        self.mock_password_file.read_text.return_value = "test-password"
        self.addCleanup(self.password_file.stop)

        self.connection = patch("minecraft_rcon.MCRcon")
        self.mock_mcrcon = self.connection.start()
        self.mock_client = self.mock_mcrcon.return_value
        self.mock_client.command.return_value = "test response"
        self.addCleanup(self.connection.stop)

    def test_connect_and_disconnect(self):
        with MinecraftRcon() as mc:
            self.mock_mcrcon.assert_called_once_with(
                "127.0.0.1",
                "test-password",
                port=25575,
            )
            self.mock_client.connect.assert_called_once()
            self.assertIsNotNone(mc._connection)

        self.mock_client.disconnect.assert_called_once()

    def test_command_forwards_request(self):
        with MinecraftRcon() as mc:
            response = mc.command("list")

        self.mock_client.command.assert_called_once_with("list")
        self.assertEqual(response, "test response")

    def test_command_without_connection(self):
        mc = MinecraftRcon()

        with self.assertRaisesRegex(RuntimeError, "not connected"):
            mc.command("list")

    def test_get_player_position(self):
        self.mock_client.command.return_value = (
            "Scrooge has the following entity data: "
            "[62.99d, 62.0d, -25.14d]"
        )

        with MinecraftRcon() as mc:
            position = mc.get_player_position("Scrooge")

        self.assertAlmostEqual(position[0], 62.99)
        self.assertAlmostEqual(position[1], 62.0)
        self.assertAlmostEqual(position[2], -25.14)

    def test_get_player_rotation(self):
        self.mock_client.command.return_value = (
            "Scrooge has the following entity data: "
            "[-87.6f, 17.1f]"
        )

        with MinecraftRcon() as mc:
            rotation = mc.get_player_rotation("Scrooge")

        self.assertAlmostEqual(rotation[0], -87.6)
        self.assertAlmostEqual(rotation[1], 17.1)

    def test_invalid_position_response(self):
        self.mock_client.command.return_value = "Unexpected response"

        with MinecraftRcon() as mc:
            with self.assertRaisesRegex(
                RuntimeError, "Could not read position"
            ):
                mc.get_player_position("Scrooge")

    def test_invalid_rotation_response(self):
        self.mock_client.command.return_value = "Unexpected response"

        with MinecraftRcon() as mc:
            with self.assertRaisesRegex(
                RuntimeError, "Could not read rotation"
            ):
                mc.get_player_rotation("Scrooge")


if __name__ == "__main__":
    unittest.main()

