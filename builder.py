
from math import floor, sin, cos, radians

from minecraft_rcon import MinecraftRcon


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


def build_wall(mc: MinecraftRcon, settings):
    px, py, pz = mc.get_player_position(PLAYER)
    yaw, _pitch = mc.get_player_rotation(PLAYER)

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


def build_gate(mc: MinecraftRcon, settings):
    px, py, pz = mc.get_player_position(PLAYER)
    yaw, _pitch = mc.get_player_rotation(PLAYER)

    yaw_rad = radians(yaw)
    forward_x = -sin(yaw_rad)
    forward_z = cos(yaw_rad)

    center_x = floor(px + forward_x * settings["distance"])
    center_z = floor(pz + forward_z * settings["distance"])

    width = settings["width"]
    height = settings["height"]
    opening_width = settings["opening_width"]
    opening_height = settings["opening_height"]
    block = settings["block"]

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

    opening_start = (width - opening_width) // 2
    opening_end = opening_start + opening_width

    print(f"Building gate: {settings['name']}")
    print(f"Player: ({px:.1f}, {py:.1f}, {pz:.1f})")
    print(f"Gate center: ({center_x}, {center_z})")
    print(
        f"Dimensions: {width} x {height}; "
        f"opening: {opening_width} x {opening_height}"
    )

    built = 0

    for i, (x, z) in enumerate(columns):
        ground_y = find_ground(
            mc,
            x,
            z,
            py,
            settings["search_above"],
            settings["search_below"],
        )

        if ground_y is None:
            print(f"Skipping ({x}, {z}): ground not found")
            continue

        base_y = ground_y + 1
        top_y = base_y + height - 1

        if opening_start <= i < opening_end:
            # Leave the opening clear and place only the lintel.
            lintel_y = base_y + opening_height

            result = mc.command(
                f"setblock {x} {lintel_y} {z} {block}"
            )

            success = (
                "block placed" in result.lower()
                or "block updated" in result.lower()
                or "no change" in result.lower()
            )
        else:
            # Build a full-height side section.
            result = mc.command(
                f"fill {x} {base_y} {z} "
                f"{x} {top_y} {z} {block}"
            )

            success = "successfully filled" in result.lower()

        if success:
            built += 1
        else:
            print(f"Column ({x}, {z}): {result}")

    print(f"Finished: {built} of {width} columns built.")
    return 0 if built == width else 1
