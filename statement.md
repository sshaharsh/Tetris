# Tkinter Tetris – Project Statement

This project is a simple implementation of the classic Tetris game using Python and Tkinter.

## Purpose

- Practice object‑oriented programming in Python.
- Learn how to build an interactive GUI application with Tkinter.
- Implement core Tetris mechanics: falling pieces, rotation, collision detection, line clearing, scoring, and level progression.

## Features

- 10x20 Tetris grid rendered on a Tkinter `Canvas`.
- Seven standard Tetris tetrominoes (I, J, L, O, S, T, Z), each with color and rotation states.
- Keyboard controls:
  - Left arrow: move piece left.
  - Right arrow: move piece right.
  - Down arrow: soft drop (faster fall).
  - Up arrow: rotate piece.
  - Space bar: hard drop (instantly place the piece).
- Next piece preview in a side panel.
- Score and level display:
  - Score increases based on the number of lines cleared at once and current level.
  - Level increases every 10 cleared lines; falling speed increases accordingly.
- Game over detection when a new piece collides on spawn.

## How It Works

- The game board is stored as a 2D list of colors representing each cell.
- The active piece is defined by:
  - Its shape type (I, J, L, O, S, T, Z).
  - Its current rotation index.
  - Its position (row, column) in the grid.
- Each shape has a list of relative coordinate offsets for its rotation states.
- On each game tick:
  - The active piece attempts to move down by one row.
  - If a collision is detected, the piece is locked into the grid.
  - Full lines are detected and removed; the grid is compressed downward.
  - Score, level, and speed are updated, and a new piece spawns.
- The main loop is driven by Tkinter’s `after` method, which repeatedly advances the game and redraws the canvas.

## Requirements

- Python 3.x
- Standard library only (uses Tkinter; no external dependencies).


