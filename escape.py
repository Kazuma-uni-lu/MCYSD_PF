from escaperoom.engine import GameEngine

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--start", default="intro")
parser.add_argument("--data", default="data")
parser.add_argument("--transcript", default="run.txt")

args = parser.parse_args()

game = GameEngine(args.data, args.start, args.transcript)

game.run()