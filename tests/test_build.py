
import tempfile
import unittest
from pathlib import Path

from build import CONFIG_DIR, load_config


VALID_CONFIG = """\
[building]
name = test_wall
type = wall

[placement]
distance = 3
surface_search_above = 6
surface_search_below = 20

[dimensions]
width = 12
height = 5

[materials]
block = stone
"""


class TestLoadConfig(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for path in self.temp_files:
            path.unlink(missing_ok=True)

    def create_config(self, content):
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".conf",
            dir=CONFIG_DIR,
            delete=False,
        ) as file:
            file.write(content)
            path = Path(file.name)

        self.temp_files.append(path)
        return path.name

    def test_valid_config(self):
        settings = load_config("gate_01.conf")

        self.assertEqual(settings["width"], 12)
        self.assertEqual(settings["height"], 5)
        self.assertEqual(settings["distance"], 3)
        self.assertEqual(settings["block"], "minecraft:stone")

    def test_missing_file(self):
        with self.assertRaises(ValueError):
            load_config("missing_test_config.conf")

    def test_path_outside_config_directory(self):
        with self.assertRaises(ValueError):
            load_config("../build_wall.py")

    def test_missing_section(self):
        filename = self.create_config(
            "[building]\n"
            "type = wall\n"
        )

        with self.assertRaisesRegex(ValueError, "Missing"):
            load_config(filename)

    def test_invalid_width(self):
        content = VALID_CONFIG.replace("width = 12", "width = 0")
        filename = self.create_config(content)

        with self.assertRaisesRegex(ValueError, "width"):
            load_config(filename)

    def test_invalid_height(self):
        content = VALID_CONFIG.replace("height = 5", "height = 101")
        filename = self.create_config(content)

        with self.assertRaisesRegex(ValueError, "height"):
            load_config(filename)

    def test_unsupported_material(self):
        content = VALID_CONFIG.replace(
            "block = stone",
            "block = diamond_block",
        )
        filename = self.create_config(content)

        with self.assertRaisesRegex(ValueError, "Unsupported block"):
            load_config(filename)

    def test_invalid_surface_search(self):
        content = VALID_CONFIG.replace(
            "surface_search_above = 6",
            "surface_search_above = 101",
        )
        filename = self.create_config(content)

        with self.assertRaisesRegex(ValueError, "surface_search_above"):
            load_config(filename)

    def test_valid_gate_config(self):
        content = VALID_CONFIG.replace(
            "type = wall",
            "type = gate",
        ) + (
            "\n[gate]\n"
            "opening_width = 4\n"
            "opening_height = 4\n"
        )

        filename = self.create_config(content)
        settings = load_config(filename)

        self.assertEqual(settings["type"], "gate")
        self.assertEqual(settings["width"], 12)
        self.assertEqual(settings["height"], 5)
        self.assertEqual(settings["opening_width"], 4)
        self.assertEqual(settings["opening_height"], 4)

    def test_opening_width_must_be_positive(self):
        content = VALID_CONFIG.replace(
            "type = wall",
            "type = gate",
        ) + (
            "\n[gate]\n"
            "opening_width = 0\n"
            "opening_height = 4\n"
        )

        filename = self.create_config(content)

        with self.assertRaisesRegex(ValueError, "opening_width"):
            load_config(filename)

    def test_opening_must_fit_inside_building(self):
        content = VALID_CONFIG.replace(
            "type = wall",
            "type = gate",
        ) + (
            "\n[gate]\n"
            "opening_width = 12\n"
            "opening_height = 4\n"
        )

        filename = self.create_config(content)

        with self.assertRaises(ValueError):
            load_config(filename)

if __name__ == "__main__":
    unittest.main()

