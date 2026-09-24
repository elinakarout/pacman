*This project has been created as part of the 42 curriculum by ekarout, kchami.*

# Pac-Craft

## Description

A Minecraft-themed recreation of the arcade game Pac-Man in Python with `pygame`. It has 10 levels of generated mazes, four ghosts with distinct behaviours, a persistent top-10 highscore list, a JSON configuration file, and a cheat mode for peer review.

Play it: <!-- TODO: unlisted Itch.io URL -->

## Instructions

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/).

```
make install    # install dependencies
make run        # uv run pac-man.py config.json
make debug      # run under pdb
make lint       # flake8 + mypy
make clean      # remove caches
```

Or directly: `uv run pac-man.py <config.json>` (exactly one argument).

**Controls:** arrows or WASD to move, `P` to pause, `Esc` to go back to the main menu.

**Cheats** (any use marks the run as cheated): `I` invincible, `E` ghosts always edible, `F` freeze ghosts, `L` skip level, `-` slower ghosts, `=` faster player, `G` add a ghost, `X` extra life.

## Configuration

JSON file; lines starting with `#` are comments. Missing keys fall back to the default with a message; invalid values (non-positive numbers) stop the game with a clear message, and unknown keys are ignored.

| Key | Default | Meaning |
|-----|---------|---------|
| `highscore_filename` | `highscore.json` | Highscore file |
| `lives` | 3 | Starting lives |
| `points_per_pacgum` | 10 | Points per pacgum |
| `points_per_super_pacgum` | 50 | Points per super-pacgum |
| `points_per_ghost` | 200 | Points per edible ghost |
| `width`, `height` | 21, 21 | Maze size in cells |
| `seed` | 42 | Seed of the first level's maze |

Levels (10) and the timer (100 s, 5 s less each level) are fixed in the code.

## Highscore

A JSON list of `{"name", "score"}` entries in `highscore_filename`, sorted by score and cut to the top 10. It is written when the player enters a name on the game-over or victory screen, and read by the Highscores menu. A missing or corrupt file is treated as empty. JSON was chosen because it is human-readable and needs no extra dependency.

## Maze Generation

Mazes come from the assigned `mazegenerator` package (`MazeGenerator`), installed from the provided wheel and used unmodified (`pyproject.toml`). `Level` calls it with `size=(width, height)` and `perfect` left at its default `False`, so corridors have loops. Level 1 uses the configured `seed`; later levels are random. Each cell is a 4-bit wall mask, which `Level` renders as wall sprites; fully closed cells (the package's "42" pattern) are drawn as blocked water tiles.

## Implementation

- **Player:** grid movement with a queued direction; it keeps going until it hits a wall. Starts in the middle and respawns there after losing a life.
- **Ghosts:** a state machine (`wait` → `chase` → `edible` → `wait` when eaten) with BFS pathfinding. Blinky targets the player, Pinky targets four cells ahead, Inky targets a point mirrored around Blinky, and Clyde chases when far and returns to his corner when close. Edible ghosts flee for 8 s.
- **Gameplay:** pacgums fill every open cell, super-pacgums sit in the four corners, and score and lives carry over between levels. Time out or zero lives ends the game.

## General Software Architecture

```
pac-man.py            entry point: Parser -> Config -> Game
src/config/           Parser (JSON + comments, defaults) and Config (pydantic validation), CHEATS flags
src/rendering/        Game (scene manager) and the scenes: MainMenu, Level, Highscore, Instructions, GameEnd
src/entities/         Player, Ghost / Ghosts
pacraft_assets/       sprites and audio    # All sprites were drawn by kchami
```

`Game` holds one scene per name; each scene's `start()` runs its loop and returns the name of the next scene (`main`, `start`, `highscore`, `instructions`, `winner:<score>`, `loser:<score>`, `exit`). All scenes derive from `CustomSurface`.

## Project Management

Method, team and tools are described in [project_management.md](project_management.md). We worked in pairs on feature branches merged through pull requests, meeting every day.

## Resources

- [pygame documentation](https://www.pygame.org/docs/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [The Pac-Man Dossier](https://pacman.holenet.info/) (ghost behaviour)
- [uv documentation](https://docs.astral.sh/uv/)

**AI usage:**

AI was used for some concept clarifications, and README skeleton
