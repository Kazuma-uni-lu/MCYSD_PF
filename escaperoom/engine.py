from escaperoom.rooms.base import GameState
from escaperoom.rooms.soc import SocRoom
from escaperoom.rooms.dns import DnsRoom
from escaperoom.rooms.vault import VaultRoom
from escaperoom.rooms.malware import MalwareRoom

from escaperoom.transcript import Transcript

import json
import hmac
import hashlib


class GameEngine:

    def __init__(self, data_path, start_room="intro", transcript_path="run.txt"):

        self.state = GameState(current_room=start_room)
        self.rooms = {
            "soc": SocRoom(data_path),
            "dns": DnsRoom(data_path),
            "vault": VaultRoom(data_path),
            "malware": MalwareRoom(data_path)
        }
        self.transcript = Transcript(transcript_path)
        self.data_path = data_path

    def look(self):

        if self.state.current_room == "intro":
            print("You are in the Intro Lobby.")
            print("A terminal blinks in the corner. Doors lead to: soc, dns, vault, malware, final.")

        elif self.state.current_room == "final":
            print("You stand before the Final Gate. The console asks for proof.")

        else:
            room = self.rooms[self.state.current_room]
            print(room.description)

    def move(self, room_name):

        if room_name in self.rooms or room_name in ("intro", "final"):

            self.state.current_room = room_name
            self.look()

        else:
            print("Unknown room.")

    def inspect(self, item):

        current = self.state.current_room

        if current not in self.rooms:
            print("Nothing to inspect here.")
            return

        room = self.rooms[current]

        if item != room.item:
            print("Item not found.")
            return

        if room.token_name in self.state.tokens:
            print("Token already collected.")
            return

        result = room.solve(self.state)

        for line in result:
            self.transcript.write(line)

    def inventory(self):

        if not self.state.inventory:
            print("Your inventory is empty.")
        else:
            print("You currently hold:", ", ".join(sorted(self.state.inventory)))

    def save(self, filename):
        
        data = {
            "current_room": self.state.current_room,
            "inventory": list(self.state.inventory),
            "tokens": self.state.tokens
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)

        print(f"[Game] Progress saved.")

    def load(self, filename):
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

        except FileNotFoundError:
            print("Filename " + filename + " does not exist!")
            return

        except OSError as e:
            print(f"File error: {e}")
            return

        except UnicodeDecodeError:
            print("File is not readable!")
            return

        self.state.current_room = data["current_room"]
        self.state.inventory = set(data["inventory"])
        self.state.tokens = data["tokens"]

        print(f"[Game] Progress loaded.")    

    def run(self):

        print("[Game] Cyber Escape Room started. Type 'help' for commands.")

        while True:

            command = input("> ").strip()

            if command == "look":
                self.look()

            elif command.startswith("move "):
                room_name = command.split(" ", 1)[1]
                self.move(room_name)

            elif command.startswith("inspect "):
                item = command.split(" ", 1)[1]
                self.inspect(item)

            elif command == "inventory":
                self.inventory()

            elif command == "quit":
                print("[Game] Goodbye.")
                break

            elif command == "help":
                print("Available commands: look, move, inspect, inventory, quit")

            elif command.startswith("save "):
                filename = command.split(" ", 1)[1]
                self.save(filename)

            elif command.startswith("load "):
                filename = command.split(" ", 1)[1]
                self.load(filename)

            elif command == "use gate":
                self.use_gate()

            else:
                print("Unknown command.")

    def use_gate(self):

        config ={}

        if self.state.current_room != "final":
            print("You must be in the Final Gate room.")
            return
    
        with open(self.data_path +"/"+ "final_gate.txt", "r", encoding="utf-8") as f:
            for line in f:
                key, value = line.strip().split("=")
                config[key] = value

        token_order = config["token_order"].split(",")

        token_ordered_values = []
        missing_tokens = []

        for token in token_order:

            if token not in self.state.tokens:
                missing_tokens.append(token)
                
            else:
                token_ordered_values.append(self.state.tokens[token])

        if missing_tokens:
            print("Missing tokens:", ", ".join(missing_tokens))
            return

        group_id = config["group_id"]
        kmac_key = config["hmac_key"]

        message = group_id + "|" + "-".join(token_ordered_values)

        digest = hmac.new(kmac_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()


        collected_tokens = []

        for token in token_order:
            collected_tokens.append(token + "=" + self.state.tokens[token])

        print("Collected tokens: " + ", ".join(collected_tokens))
        
        self.transcript.write("FINAL_GATE=PENDING")
        self.transcript.write("MSG="+message)
        self.transcript.write("HMAC="+digest)

    #TODO add hint() function

if __name__ == "__main__":

    game = GameEngine("data")
    game.run()

    '''
    game.look()

    game.move("soc")
    game.inspect("auth.log")

    game.inventory()

    game.move("dns")
    game.inspect("dns.cfg")

    game.inventory()

    game.move("vault")
    game.inspect("vault_dump.txt")

    game.move("malware")
    game.inspect("proc_tree.jsonl")

    game.inventory()


    print(game.state.tokens)
    print("*******************************************")
    #print(game.rooms["vault"].item == "vault_dump.txt")
    #print(game.rooms["malware"].item == "proc_tree.jsonl")
    '''