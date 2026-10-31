# AI Context — Minecraft Builder

**Last updated:** 2026-10-31

## 1. Project Overview

Minecraft Builder is a Python-based tool for constructing structures in Minecraft using RCON commands.

The project is designed to build structures from configuration files. Current structure types include walls and gates. The architecture should support additional structure types in the future.

The project owner works on this project part-time. Important decisions, architecture changes, and task progress must therefore be documented so work can be resumed after long breaks.

## 2. Development Environment

- OS: Linux Mint 21.3 Cinnamon
- Python: 3.10.12
- Minecraft server: Paper 1.21.11
- Minecraft edition: Java Edition
- RCON host: 127.0.0.1
- RCON port: 25575
- Python project directory: `~/minecraft-lab/python/`

## 3. Current Project Structure

Known project files:

- `build.py` — command-line entry point and configuration loading.
- `builder.py` — structure construction algorithms.
- `minecraft_rcon.py` — Minecraft RCON communication.
- `configs/` — structure configuration files.
- `tests/` — automated tests.
- `build_wall.py` — legacy prototype.
- `check_ground.py` — diagnostic utility.
- `test_rcon.py` — RCON diagnostic utility.

AI project documentation is stored separately under `docs/ai/`.

## 4. Current Architecture Direction

The project is moving toward a shared construction workflow:

1. Determine the building volume from the player's position and facing direction.
2. Validate the dimensions and coordinates.
3. Clear the entire building volume.
4. Build the requested structure.
5. Verify the result.

All structure types should reuse common positioning and preparation logic wherever practical.

## 5. Accepted Architectural Decisions

The authoritative decisions are recorded in `docs/ai/DECISIONS.md`.

Currently accepted:

- **DEC-001:** Gates have a continuous wall above the lintel, extending to the full configured height.
- **DEC-002:** The entire building volume is cleared before construction, including bottom and top boundaries.
- **DEC-003:** Structures are positioned relative to the player's location and facing direction.

Do not contradict or silently reinterpret accepted decisions. If an implementation detail is ambiguous, identify it and ask the Project Owner.

## 6. Development and Change-Control Rules

- The Project Owner has final decision-making authority.
- AI models may analyze and propose changes.
- AI models must not independently modify project files.
- All source-code changes are applied manually by the Project Owner through VS Code.
- Tests must be run after implementation changes.
- Existing functionality must not be unintentionally broken.
- Avoid unrelated refactoring.
- Update project documentation when an important decision or implementation change is accepted.

## 7. Current Known Test Status

The latest review available (2026-10-31) reported 22 passing unit tests across:

- `test_build.py`
- `test_builder.py`
- `test_minecraft_rcon.py`

This is a historical result, not a guarantee that the current working tree still passes.

## 8. Important Notes

The current implementation may not yet follow the accepted architectural decisions.

Do not assume that a decision has already been implemented merely because it is documented.

Before proposing code changes, inspect the current source files and compare the implementation with `DECISIONS.md`.
