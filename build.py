
import configparser
import sys
from pathlib import Path

from mcrcon import MCRconException

from builder import build_gate, build_wall
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

    building_type = config["building"].get("type", "").strip()

    if building_type not in {"wall", "gate"}:
        raise ValueError(
            "Unsupported building type: "
            f"{building_type or '(empty)'}"
        )

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
        raise ValueError(
            "surface_search_above must be between 0 and 100"
        )

    if not 0 <= search_below <= 100:
        raise ValueError(
            "surface_search_below must be between 0 and 100"
        )

    block = config["materials"].get("block", "").strip()

    if block.startswith("minecraft:"):
        block = block.removeprefix("minecraft:")

    if block not in ALLOWED_BLOCKS:
        raise ValueError(f"Unsupported block material: {block}")

    opening_width = None
    opening_height = None

    if building_type == "gate":
        if "gate" not in config:
            raise ValueError("Missing [gate] section")

        opening_width = config.getint("gate", "opening_width")
        opening_height = config.getint("gate", "opening_height")

        if not 1 <= opening_width < width:
            raise ValueError(
                "opening_width must be positive and less than width"
            )

        if not 1 <= opening_height < height:
            raise ValueError(
                "opening_height must be positive and less than height"
            )

    return {
        "name": config["building"].get("name", "unnamed"),
        "type": building_type,
        "width": width,
        "height": height,
        "distance": distance,
        "search_above": search_above,
        "search_below": search_below,
        "block": f"minecraft:{block}",
        "opening_width": opening_width,
        "opening_height": opening_height,
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

    builders = {
        "wall": build_wall,
        "gate": build_gate,
    }

    try:
        with MinecraftRcon() as mc:
            return builders[settings["type"]](mc, settings)
    except (MCRconException, OSError, RuntimeError, ValueError) as error:
        print(f"Minecraft/RCON error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
