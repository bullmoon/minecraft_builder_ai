import configparser
import sys
from pathlib import Path

from mcrcon import MCRconException

from builder import build_wall
from minecraft_rcon import MinecraftRcon


CONFIG_DIR = Path(__file__).resolve().parent / "configs"

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
    with path.open(encoding="utf-8") as file:
        config.read_file(file)

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

    search_above = config.getint(
        "placement", "surface_search_above", fallback=6
    )
    search_below = config.getint(
        "placement", "surface_search_below", fallback=20
    )

    if not 0 <= search_above <= 100:
        raise ValueError("surface_search_above must be between 0 and 100")
    if not 0 <= search_below <= 100:
        raise ValueError("surface_search_below must be between 0 and 100")

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
        "search_above": search_above,
        "search_below": search_below,
        "block": f"minecraft:{block}",
    }


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python build.py <config.conf>\n"
            "Example: python build.py gate_01.conf"
        )
        return 2

    try:
        settings = load_config(sys.argv[1])
    except (ValueError, OSError, configparser.Error) as error:
        print(f"Configuration error: {error}")
        return 2

    try:
        with MinecraftRcon() as mc:
            return build_wall(mc, settings)
    except (MCRconException, OSError, RuntimeError, ValueError) as error:
        print(f"Minecraft/RCON error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

