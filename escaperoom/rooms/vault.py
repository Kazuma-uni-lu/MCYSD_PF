from escaperoom.rooms.base import GameState,Room


import re
'''
https://docs.python.org/3/howto/regex.html  guide
https://docs.python.org/3/library/re.html
https://regex101.com use this to test regex 

\s => whitespace
\d => digits
* zero or more
+ at least once
\{\} escape sequence for {}
(...) matches and indicates the start and end of a group; the contents of a group can be retrieved after a match has been performed
https://docs.python.org/3/library/re.html#re.Match.group
https://docs.python.org/3/library/re.html#search-vs-match
'''

#vault -> SAFE
#soc, dns, vault, malware, final
class VaultRoom(Room):
    pattern = re.compile(r"SAFE\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}")
    path = 'data/vault_dump.txt'
    def __init__(self,path):
        super().__init__(
            name = "vault",
            description = "You enter the Vault Corridor.\nA noisy dump scrolls past. Somewhere a SAFE{a-b-c} hides.\nItems here: vault_dump.txt",
            item = "vault_dump.txt",
            path = path,
            token_name = "SAFE"
        )
    def solve(self, state: GameState) -> tuple[str,list[int]]:
        file_path = self.path + self.item
        found = None
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                pattern_match = re.search(self.pattern,line) #assuming there is no more than one match per line (from txt file)
                if pattern_match:
                    candidate = [int(pattern_match.group(i)) for i in range(1,4)]
                    if sum(candidate[:-1]) ==  candidate[-1]:
                        evidence = pattern_match.group(0)
                        found = (evidence, candidate)
                        break
        if found is None:
            raise ValueError("No candidates found")
        evid, a, b, c = found
        token = f"{a}-{b}-{c}"
        
        state.tokens[self.token_name] = token
        state.inventory.add(self.token_name)

        return [
            f"TOKEN[{self.token_name}]={token}"
            f"EVIDENCE[{self.token_name}].MATCH={evid}"
            f"EVIDENCE[{self.token_name}].CHECK={a}+{b}={c}"
        ]











