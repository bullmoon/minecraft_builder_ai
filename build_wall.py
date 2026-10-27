
import configparser
from math import floor, sin, cos, radians
from pathlib import Path
import re
import sys

from mcrcon import MCRcon


BASE_DIR = Path.home() / "minecraft-lab"
CONFIG_DIR = BASE_DIR / "python" / "configs"
PASSWORD_FILE = (
    Path.home() / ".config/minecraft-lab/rcon_password"
)

PLAYER = "Scrooge"

NON_SOLID = (
    "air", "cave_air", "void_air", "water", "lava",
    "grass", "tall_grass", "fern", "large_fern",
    "seagrass", "tall_seagrass", "kelp", "kelp_plant",
    "snow", "vine", "glow_lichen", "dead_bush",
)

GROUND_BLOCKS = (
    "grass_block", "dirt", "coarse_dirt", "rooted_dirt",
    "podzol", "mycelium", "stone", "granite", "diorite",
    "andesite", "deepslate", "tuff", "gravel", "sand",
    "red_sand", "clay", "mud", "moss_block", "snow_block",
    "sandstone", "red_sandstone", "terracotta",
    "netherrack", "end_stone", "bedrock",
)

ALLOWED_BLOCKS = {
    "stone", "cobblestone", "bricks", "stone_bricks",
    "glass", "oak_planks", "spruce_planks", "birch_planks",
    "quartz_block", "smooth_stone", "deepslate_bricks",
    "dirt", "grass_block", "sandstone", "polished_andesite",
}


def load_config(filename):
    path = (CONFIG_DIR / filename).resolve()

    if path.parent != CONFIG_DIR.resolve():
        raise ValueError("Config must be inside the configs directory.")

    if not path.is_file() or path.suffix != ".conf":
        raise ValueError(f"Config file not found: {path}")

    config = configparser.ConfigParser()
    config.read(path)

    required_sections = (
        "building", "placement", "dimensions", "materials"
    )
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing [{section}] section")

    if config["building"].get("type") != "wall":
        raise ValueError("Currently supported building type: wall")

    width = config.getint("dimensions", "width")
    height = config.getint("dimensions", "height")
    distance = config.getint("placement", "distance")

    if not 1 <= width <= 100:
        raise ValueError("width must be between 1 and 100")
    if not 1 <= height <= 100:
        raise ValueError("height must be between 1 and 100")
    if not 1 <= distance <= 20:
        raise ValueError("distance must be between 1 and 20")

    block = config["materials"].get("block", "").strip()
    if block.startswith("minecraft:"):
        block = block.removeprefix("minecraft:")

    if block not in ALLOWED_BLOCKS:
        raise ValueError(f"Unsupported block material: {block}")

    return {
        "name": config["building"].get("name", "unnamed"),
        "width": width,
        "height": height,
        "distance": distance,
        "search_above": config.getint(
            "placement", "surface_search_above", fallback=6
        ),
        "search_below": config.getint(
            "placement", "surface_search_below", fallback=20
        ),
        "block": f"minecraft:{block}",
    }


def block_matches(mc, x, y, z, block):
    result = mc.command(
        f"execute if block {x} {y} {z} minecraft:{block}"
    )
    return "test passed" in result.lower()


def find_ground(mc, x, z, player_y, above, below):
    top = floor(player_y) + above
    bottom = floor(player_y) - below

    for y in range(top, bottom - 1, -1):
        if any(
            block_matches(mc, x, y, z, block)
            for block in NON_SOLID
        ):
            continue

        for block in GROUND_BLOCKS:
            if block_matches(mc, x, y, z, block):
                return y

    return None


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python build_wall.py <config.conf>\n"
            "Example: python build_wall.py gate_01.conf"
        )
        return 2

    try:
        settings = load_config(sys.argv[1])
    except (ValueError, OSError, configparser.Error) as error:
        print(f"Configuration error: {error}")
        return 2

    password = PASSWORD_FILE.read_text().strip()

    with MCRcon("127.0.0.1", password, port=25575) as mc:
        position = mc.command(f"data get entity {PLAYER} Pos")
        rotation = mc.command(f"data get entity {PLAYER} Rotation")

        pos_match = re.search(
            r"\[([-0-9.]+)d?,\s*([-0-9.]+)d?,\s*([-0-9.]+)d?\]",
            position,
        )
        rot_match = re.search(
            r"\[([-0-9.]+)f?,\s*([-0-9.]+)f?\]",
            rotation,
        )

        if not pos_match or not rot_match:
            raise RuntimeError(
                f"Could not read player position/direction:\n"
                f"{position}\n{rotation}"
            )

        px, py, pz = map(float, pos_match.groups())
        yaw, _pitch = map(float, rot_match.groups())

        yaw_rad = radians(yaw)
        forward_x = -sin(yaw_rad)
        forward_z = cos(yaw_rad)

        center_x = floor(px + forward_x * settings["distance"])
        center_z = floor(pz + forward_z * settings["distance"])

        width = settings["width"]

        if abs(forward_x) > abs(forward_z):
            columns = [
                (center_x, center_z + i - width // 2)
                for i in range(width)
            ]
        else:
            columns = [
                (center_x + i - width // 2, center_z)
                for i in range(width)
            ]

        print(f"Building: {settings['name']}")
        print(f"Player: ({px:.1f}, {py:.1f}, {pz:.1f})")
        print(f"Wall center: ({center_x}, {center_z})")

        built = 0

        for x, z in columns:
            ground_y = find_ground(
                mc, x, z, py,
                settings["search_above"],
                settings["search_below"],
            )

            if ground_y is None:
                print(f"Skipping ({x}, {z}): ground not found")
                continue

            base_y = ground_y + 1
            top_y = base_y + settings["height"] - 1

            result = mc.command(
                f"fill {x} {base_y} {z} "
                f"{x} {top_y} {z} {settings['block']}"
            )

            if "successfully filled" in result.lower():
                built += 1
            else:
                print(f"Column ({x}, {z}): {result}")

        print(f"Finished: {built} of {width} columns built.")
        return 0 if built == width else 1


if __name__ == "__main__":
    raise SystemExit(main())

