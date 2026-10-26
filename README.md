# Cyber Escape Room Project (Group 5)

<ins>Note:</ins> This README was written with the help of Claude Sonnet 5.5

This is an Escape Room Game where you solve puzzles in order to advance to the next room. Inspect and extract clues and most importantly, have fun!

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
## How to play

Use the following commands to take various actions that are necessary to traverse and complete the game:

```
look
move <room>
inspect <item>
use <item>
inventory
hint
save <file>
load <file>
quit
```

## What the commands do

|Command| Action |
|-------|--------|
|look| describes the room you are currently in or what rooms are available for inspection |
|move `<room>`| lets you change rooms|
|inspect `<item>`| tells you if you already collected the item from the room or not
|use `<item>`| checks whether the final gate room is reached, lists if any tokens are missing and if all rooms have been completed it creates a key to end the game
|inventory| shows all items currently in possession
|hint| describes what you must do in order to solve the room
|save `<file>`| allows you to save your progress
|load `<file>`| allows you to load the progress from a desired savefile
|quit| closes the game

