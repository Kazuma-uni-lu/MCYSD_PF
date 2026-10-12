from datetime import datetime
import ipaddress, os

from escaperoom.rooms.base import GameState,Room

logs = []
valid_logs = []

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        print(f"Reading file: {filename}")
        for line in file:
            logs.append(line.strip().split())
            #print(line)
           
def daytime_valid(date_time):
    try:
        datetime.fromisoformat(date_time)
        return True
    except ValueError:
        return False

def pid_port_valid(sshd_pid, port_nbr):
    try:
        pid_nbr = sshd_pid.split('[')[1].split(']')[0]
    except IndexError:
        return False

    try:
        int(pid_nbr)
        int(port_nbr)
        return True
    except ValueError:
        return False

def ipaddress_valid(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        #print(f"Invalid IP address: {ip}")
        return False

def check_valid_entry():
    invalid_count = 0
    for i in range(len(logs)): # check if format is valid for each log entry
        if (
            len(logs[i]) == 13 
            and daytime_valid(logs[i][0]) == True
            and pid_port_valid(logs[i][2], logs[i][10]) == True
            and ipaddress_valid(logs[i][8]) == True
        ):
            valid_logs.append(logs[i])
        else:
            invalid_count += 1
    print(f"Valid entries: {len(valid_logs)}")
    print(f"Invalid entries: {invalid_count}")

    return invalid_count

def failed_login():
   
    ips = []
    subnets = {}
    for log in valid_logs:
        if log[3] == "Failed":
            ips.append(log[8])

    for ip in ips:
        tmp = ".".join(ip.split('.')[0:3]) # tmp represents the first 3 octets of the ip, which is the key for the dictionary
        if tmp in subnets:
            subnets[tmp] += 1
        else:
            subnets[tmp] = 1
    print(f"Subnets with failed logins: {subnets}")
    print(f"Max failed logins from a subnet: {max(subnets.values())}")

    max_subnet=""

    for subnet, count in subnets.items():
        if count == max(subnets.values()):
            max_subnet = subnet
            #print(f"Subnet with max failed logins: {subnet}.0/24 ({count} failed logins)")

    max_subnet_ips = []

    for ip in ips:
        if ip.startswith(max_subnet):
            max_subnet_ips.append(ip)

    max_freq_ip = {}

    for ip in max_subnet_ips:
        if ip in max_freq_ip:
            max_freq_ip[ip] += 1
        else:
            max_freq_ip[ip] = 1

    octet = ""
    count = subnets[max_subnet] # Total failed logins for the chosen winning subnet
    chosen_ip = ""

    for ip, freq in max_freq_ip.items():
        if freq == max(max_freq_ip.values()):
            octet = ip.split('.')[3]
            
            chosen_ip = ip
            #print(f"IP with max failed logins in subnet {max_subnet}.0/24: {ip} ({freq} failed logins)")

    sample_entry = ""

    for log in valid_logs:
        if log[3] == "Failed" and log[8] == chosen_ip:
            sample_entry = " ".join(log)

            break # when first match is found, stop the loop, otherise the last match will be taken
    return octet, count, max_subnet, sample_entry

def keypad_gen(octet, count):
    
    keypad = octet + "" + str(count)
    #print(f"Generated keypad: {keypad}")
    return keypad

'''
def soc_transcript():

    invalid_count = check_valid_entry()

    octet, count, max_subnet, sample_entry = failed_login()

    keypad = keypad_gen(octet, count)

    text = "TOKEN[KEYPAD]=" + keypad + "\n"
    text += "EVIDENCE[KEYPAD].TOP24=" + max_subnet + ".0/24\n"
    text += "EVIDENCE[KEYPAD].COUNT=" + str(count) + "\n"
    text += "EVIDENCE[KEYPAD].SAMPLE=" + sample_entry + "\n"
    text += "EVIDENCE[KEYPAD].MALFORMED_SKIPPED=" + str(invalid_count) + "\n"

    print(text)
    #return text

read_file('MCYSD_PF/data/auth.log')
#print(logs[23][2].split('[')[1].split(']')[0]) 
#failed_login()
#keypad_gen()
soc_transcript()
'''

class SocRoom(Room):

    def __init__(self, path):
        super().__init__(
            name="soc",
            description="You enter the SOC Triage Desk.\nA cluttered screen shows failed SSH login attempts.\nItems here: auth.log"
        )

        self.path = path
        self.item = "auth.log"
        self.token_name = "KEYPAD"

    def solve(self, state: GameState):

        logs.clear()
        valid_logs.clear()

        filepath = self.path + "/" + self.item

        read_file(filepath)

        invalid_count = check_valid_entry()
        octet, count, max_subnet, sample_entry = failed_login()
        keypad = keypad_gen(octet, count)

        state.tokens[self.token_name] = keypad
        state.inventory.add(self.token_name)

        return [
            f"TOKEN[KEYPAD]={keypad}",
            f"EVIDENCE[KEYPAD].TOP24={max_subnet}.0/24",
            f"EVIDENCE[KEYPAD].COUNT={count}",
            f"EVIDENCE[KEYPAD].SAMPLE={sample_entry}",
            f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={invalid_count}",
        ]
