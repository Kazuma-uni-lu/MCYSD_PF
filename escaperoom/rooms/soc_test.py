from datetime import datetime
import ipaddress

#logs = []
#valid_logs = []

from escaperoom.rooms.base import GameState,Room
#soc -> Keypad
#soc, dns, vault, malware, final
class SocRoom(Room):
    logs = []
    valid_logs = []
    def __init__(self, path):
        super().__init__(
            name = "soc",
            description= "You enter the SOC Triage Desk.\nA cluttered screen shows failed SSH login attempts.\nItems here: auth.log",
            item = "auth.log",
            path = path,
            token_name = "Keypad"
        )
    def solve(self, state:GameState):
        self.logs = read_file(self.path + "/" + self.item)
        keypad_code = keypad_gen(self.logs,self.valid_logs)
        return [
            f"TOKEN[KEYPAD]={keypad_code}",
            f"EVIDENCE[KEYPAD].TOP24=<cidr>/24",
            f"EVIDENCE[KEYPAD].COUNT=<int>",
            f"EVIDENCE[KEYPAD].SAMPLE=<one full valid failed-login line from the winning /24>",
            f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED=<int>"
        ]
        

def read_file(filename):
    logs = []
    with open(filename, 'r', encoding='utf-8') as file:
        print(f"Reading file: {filename}")
        for line in file:
            logs.append(line.strip().split())
    return logs
           
def daytime_valid(date_time):
    try:
        datetime.fromisoformat(date_time)
        return True
    except ValueError:
        return False

def integer_check(sshd_pid, port_nbr):
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

def ipaddress_check(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        #print(f"Invalid IP address: {ip}")
        return False

def check_valid_entry(logs,valid_logs):
    invalid_count = 0
    for i in range(len(logs)):
        if (
            len(logs[i]) == 13 
            and daytime_valid(logs[i][0]) == True
            and integer_check(logs[i][2], logs[i][10]) == True
            and ipaddress_check(logs[i][8]) == True
        ):
            valid_logs.append(logs[i])
        else:
            invalid_count += 1
    print(f"Total valid entries: {len(valid_logs)}")
    print(f"Total invalid entries: {invalid_count}")

def failed_login(logs,valid_logs):
    check_valid_entry(logs,valid_logs)
    ips = []
    subnets = {}
    for log in valid_logs:
        if log[3] == "Failed":
            ips.append(log[8])

    for ip in ips:
        tmp = ".".join(ip.split('.')[0:3])
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
            print(f"Subnet with the most failed logins: {subnet}.0/24 with {count} failed logins.")

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
    count = 0

    for ip, freq in max_freq_ip.items():
        if freq == max(max_freq_ip.values()):
            octet = ip.split('.')[3]
            count = freq
            print(f"IP with the most failed logins in subnet {max_subnet}.0/24: {ip} with {freq} failed logins.")

    return octet, count

def keypad_gen(logs,valid_logs) -> list[str]:
    octet, count = failed_login(logs,valid_logs)
    keypad = octet + "" + str(count)
    print(f"Generated keypad code: {keypad}")
    return keypad

#read_file('MCYSD_PF/data/auth.log')
#print(logs[23][2].split('[')[1].split(']')[0]) 
#failed_login()
#keypad_gen()

if __name__ == "__main__":
    state = GameState()
    room = SocRoom("data")
    room.solve(state)