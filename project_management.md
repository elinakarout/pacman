# Project Management

## Overview

Pac-Man in Python, built by two teammates, Elina and Karim.

The goal was a complete playable game with config file, maze generation from the assigned A-Maze-ing package, highscores, cheat mode, and a packaged release.

We also wanted to add our creativity by going beyound the regular pac-man style.

## Team

| Person | Git identities | Main responsibilities |
|--------|----------------|-----------------------|
| Elina Karout | `ekarout` | Config parser, maze/config integration, player, pacgums and scoring, ghosts, audio, lint,cheat mode, README |
| Karim Chami | `kchami` | Maze rendering and game window, main menu and states, highscore file and window, instructions screen, sprites and font, game end screen, pause and timer, docstrings, packaging, all images used |
| Together | Both | PR Reviews, debugging, cheat mode |

## Method

### Communication

We met every day in person on campus. Priorities, task split and blockers were settled there.

### Git workflow

- One feature branch per feature, merged into `main` through a GitHub pull request.
- Branches so far: `ConfigParse`, `MazeRender`, `HighscoreWindow`, `Player`, `Pacgums`, `InstructionsWindow`, `ArtSprites`, `GameEnd`, `CheatMode` (PRs #1-#11).
- Lint was fixed alongside features, not left to the end.
- We used no task board or issue tracker; progress is visible in the branches, PRs and commit history.

### Tools

| Purpose | Tool |
|---------|------|
| Version control and PRs | Git, GitHub |
| Dependencies | `uv` |
| Quality checks | flake8, mypy (via the Makefile `lint` rule) |
| Communication | in person daily, Slack messages |
