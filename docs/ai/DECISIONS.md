### DEC-001 — Gate geometry: continuous wall above lintel

**Status:** Accepted  
**Date:** 2026-10-31

**Decision**

A gate must have a continuous wall above its lintel, extending to the full configured structure height.

**Rules**

- The opening height is measured from `base_y`.
- The lintel is placed at `base_y + opening_height`.
- All blocks above the lintel up to `base_y + height - 1` must be filled with the configured wall material.
- Both side sections extend to the full configured height.
- The opening remains clear below the lintel because the entire building volume is cleared before construction.

**Rationale**

The gate should form a continuous wall structure with a defined opening, rather than two tall pillars connected by a single isolated beam.

**Implementation impact**

- Update `build_gate()` in `builder.py`.
- Update and extend `tests/test_builder.py`.
- Add a test where `height > opening_height + 1`.

### DEC-002 — Full Building Volume Clearing

**Status:** Accepted  
**Date:** 2026-10-31

**Decision**

Before construction, the Builder completely clears the entire defined building volume, including its bottom and top boundaries.

**Rules**

- The building volume is a rectangular cuboid defined by width, length, and height.
- All existing blocks inside the volume are replaced with air.
- No block categories are excluded.
- The bottom boundary is cleared as well.
- Construction starts only after the clearing operation succeeds.
- Existing terrain, vegetation, foundations, and structures inside the volume are not preserved.
- The Builder must not modify blocks outside the defined volume.

**Implementation principles**

- Use Minecraft `fill` commands where possible.
- Split large volumes into smaller operations when required by Minecraft command limits.
- Validate volume dimensions and coordinates before clearing.
- Keep preparation and construction as separate logical operations.

**Consequences**

- Ground detection is no longer responsible for identifying every acceptable ground material.
- Gate and wall construction can use the same preparation mechanism.
- Building algorithms can assume that the defined construction volume is empty before construction begins.

### DEC-003 — Player-Relative Building Placement

**Status:** Accepted  
**Date:** 2026-10-31

**Decision**

All structures are positioned relative to the player's location and facing direction.

**Rules**

- The player stands at the selected construction location.
- The structure is built in front of the player.
- The default distance between the player and the beginning of the building volume is 3 blocks.
- The building's width is centered relative to the player's facing direction.
- The building's length extends forward from the player.
- The building's height extends upward from the player's feet level.
- The block supporting the player remains outside the building volume.
- The same positioning logic must be reusable by all structure types.

**Default Parameters**

- `build_distance = 3`
- `center_width = true`

**Consequences**

- Manual specification of absolute X, Y, and Z coordinates is not required for normal construction.
- The player's position and facing direction determine the building volume.
- Ground detection is not required to determine the base height of each individual column.
- All structure builders use the same positioning mechanism.

**Implementation impact**

- Introduce shared building-volume coordinate calculation.
- Account for the player's position, facing direction, structure dimensions, and build distance.
- Add unit tests for all four cardinal directions.
- Add tests for even and odd structure widths.
