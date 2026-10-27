# Minecraft Builder — Project Status

**Last updated:** 2026-10-27

## 1. Project goal

Develop a local Minecraft building system using Python and RCON.

The builder reads `.conf` files and constructs structures in the Minecraft world based on the player's position and direction.

Current implementation supports walls. The next planned building type is a proper gate.

## 2. Environment

- OS: Linux Mint 21.3 Cinnamon
- Python: 3.10.12
- Java: OpenJDK 21
- Minecraft server: Paper 1.21.11
- Server directory: `~/minecraft-lab/server/`
- Start script: `~/minecraft-lab/start.sh`
- Stop script: `~/minecraft-lab/stop.sh`
- Python project: `~/minecraft-lab/python/`
- Virtual environment: `~/minecraft-lab/python/.venv/`
- Python RCON library: `mcrcon`
- RCON endpoint: `127.0.0.1:25575`
- RCON password file: `~/.config/minecraft-lab/rcon_password`
- Current player name: `Scrooge`

Never print, commit, or copy the RCON password into building configuration files.

## 3. Current architecture

```text
python/
├── .gitignore
├── PROJECT_STATUS.md
├── build.py
├── builder.py
├── minecraft_rcon.py
├── build_wall.py
├── check_ground.py
├── test_rcon.py
├── configs/
│   └── gate_01.conf
└── tests/
    ├── test_build.py
    └── test_minecraft_rcon.py
```

The old `build_wall.py` and its local backup are retained for comparison and recovery.

### `build.py`

- Entry point.
- Reads command-line arguments.
- Loads and validates building configuration.
- Calls the builder.
- Handles expected configuration and RCON errors.

### `builder.py`

- Calculates building position and orientation.
- Searches for the ground surface.
- Builds walls as vertical columns.
- Reports the number of successfully built columns.

### `minecraft_rcon.py`

- Connects to Minecraft through RCON.
- Reads the password from the external password file.
- Executes server commands.
- Reads player position and rotation.

### `configs/`

Contains building definitions. These files must never contain RCON credentials.

### `tests/`

Contains automated tests for configuration loading and RCON behavior.

## 4. Current building configuration

File: `configs/gate_01.conf`

Despite its filename, this configuration currently builds a wall, not a real gate.

Current settings:

- Building name: `gate_01`
- Building type: `wall`
- Width: 12 columns
- Height: 5 blocks
- Distance from player: 3 blocks
- Surface search above player: 6 blocks
- Surface search below player: 20 blocks
- Material: `minecraft:stone`

## 5. Commands

Run commands from `~/minecraft-lab/python`.

Activate neither the virtual environment nor any other shell setup is required when using its Python executable directly.

Run the builder:

```bash
.venv/bin/python build.py gate_01.conf
```

Run all automated tests:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Check Python syntax:

```bash
.venv/bin/python -m py_compile \
    build.py builder.py minecraft_rcon.py \
    tests/test_build.py tests/test_minecraft_rcon.py
```

Test RCON against the live server:

```bash
.venv/bin/python test_rcon.py
```

The live RCON test requires the Minecraft server to be running.

## 6. Verified state

As of 2026-10-27:

- The modular builder successfully built 12 of 12 wall columns.
- Configuration validation passed.
- RCON successfully returned the player list.
- Player position and rotation were read successfully.
- All 15 automated tests passed:
  - 8 configuration tests.
  - 7 RCON tests.
- Python syntax checks passed.
- A local Git repository has been initialized.
- Initial commit: `9ce7bdd` — `Add modular Minecraft builder`.
- The working tree was clean after the initial commit.

The initial Git commit does not contain the local backup file `build_wall.py.bak-20261027-145654`.

## 7. Development rules

1. Preserve working behavior unless a change is intentional.
2. Make a backup before risky modifications.
3. Use `vim` for manual editing; do not use `nano`.
4. Give exact Linux commands and verify each stage.
5. Do not delete the old builder until the replacement is verified.
6. Keep the architecture simple.
7. Do not put credentials in configuration files or Git.
8. Run automated tests after changes.
9. Do not execute a live build during tests unless explicitly intended.
10. Keep building algorithms independent from RCON connection management.

## 8. Chat organization

Use separate chats for substantial work on different building types.

- **Infrastructure:** shared Python architecture, RCON, configuration handling, Git, and common testing.
- **Walls:** wall-specific algorithms, dimensions, materials, and wall configurations.
- **Gates:** gate geometry, openings, support columns, lintels, and future moving gate mechanisms.
- **Buildings:** foundations, floors, roofs, and multi-level structures.

A chat is a work area, not a separate codebase. All building types should reuse shared infrastructure.

## 9. Next task: implement real gates

The current `gate_01.conf` is only a wall configuration. Do not assume gate behavior already exists.

In the dedicated gate-development chat:

1. Read this project status and inspect the actual source files.
2. Confirm the existing architecture before changing code.
3. Define the required gate geometry and configuration options.
4. Design tests for gate dimensions and placement.
5. Implement the gate builder without breaking wall construction.
6. Run automated tests and verify the result in Minecraft.
7. Commit the verified changes to Git.

Keep the existing wall implementation working throughout development.

