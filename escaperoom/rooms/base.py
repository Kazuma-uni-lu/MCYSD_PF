from dataclasses import dataclass, field
'''
soc -> Keypad
dns -> DNS
vault -> SAFE
malware -> PID
'''
@dataclass
class GameState:
    current_room: str = "intro"
    inventory: set[str] = field(default_factory=set)
    tokens: dict[str, str] = field(default_factory=dict)


#soc, dns, vault, malware, final
class Room:
    def __init__(self, name: str, description: str, item: str, token_name: str, path: str, hint: str):
        self.name = name
        self.description = description
        self.item = item
        self.token_name = token_name
        self.path = path
        self.hint = hint

    def solve(self, state: GameState):
        raise NotImplementedError