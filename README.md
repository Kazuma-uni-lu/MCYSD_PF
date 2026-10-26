# Cyber Escape Room Project (Group 5)

<ins>Note:</ins> This README was written with the help of Claude Sonnet 5.5

This is an Escape Room Game where you solve puzzles in order to advance to the next room. Inspect and collect tokens from each room, then reach the final gate to finish.

## Requirements

- Python 3.10 or newer. The code uses Python syntax introduced in Python 3.10.
- No third-party packages are required; the game uses Python's standard library.

## Installation

Clone the Git repo using the following command:
```
git clone https://github.com/Kazuma-uni-lu/MCYSD_PF.git
cd MCYSD_PF
```

## How to run

Use the following command to start the Escape Room:
```
python escape.py --start intro --transcript run.txt
```
Note: Use 'python3' if 'python' doesn't work. 

### What the run flags mean

- `--start intro` sets the room where the game begins. The start room is optional; if omitted, the game uses `intro`.
- `--transcript run.txt` sets the file where the game records session events. The transcript path is optional; if omitted, the game uses `run.txt`.

## How to play

Use the following commands to take various actions that are necessary to traverse and complete the game:

|Command| Action |
|--------------|---------------|
|look| describes the room you are currently in or what rooms are available for inspection|
|move `<room>`| lets you change rooms|
|inspect `<item>`| tells you if you already collected the item from the room or not|
|use `<item>`| at the final gate, this checks whether you’ve collected all tokens and, if so, prints the tokens and builds a message and HMAC digest and writes them to the transcript which shows that the escape room was completed|
|inventory| shows all items currently in possession|
|hint| describes what you must do in order to solve the room|
|save `<file>`| allows you to save your progress to a file with a chosen filename in the current folder|
|load `<file>`| allows you to load the progress from a desired savefile using the filename in the current folder|
|quit| closes the game|

## Team

This Escape Room was developed by:
- Siléas Kazuma Hugot
- Filomeno Antunes
- Luca Neiens

## About

Created for the programming fundamentals course at University of Luxembourg.