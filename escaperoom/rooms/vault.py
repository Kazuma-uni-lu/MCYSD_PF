import re
#https://docs.python.org/3/howto/regex.html  guide
#https://docs.python.org/3/library/re.html
#https://regex101.com use this to test regex 
'''
\s => whitespace
\d => digits
* zero or more
+ at least once
\{\} escape sequence for {}
(...) matches and indicates the start and end of a group; the contents of a group can be retrieved after a match has been performed
https://docs.python.org/3/library/re.html#re.Match.group match and group
'''


pattern = re.compile(r"SAFE\s*\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}")



def solve_vault(path) -> tuple[str,list[int]]:
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            pattern_match = re.search(pattern,line) #assuming there is no more than one match per line (from txt file)
            if pattern_match:
                candidate = [int(pattern_match.group(i)) for i in range(1,4)]
                if sum(candidate[:-1]) ==  candidate[-1]:
                    evidence = pattern_match.group(0)
                    return (evidence, candidate)
            