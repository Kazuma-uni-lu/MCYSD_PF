from datetime import datetime
import ipaddress

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

def check_valid_entry():
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

def failed_login():
    check_valid_entry()
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

def keypad_gen():
    octet, count = failed_login()
    keypad = octet + "" + str(count)
    print(f"Generated keypad code: {keypad}")

read_file('MCYSD_PF/data/auth.log')
#print(logs[23][2].split('[')[1].split(']')[0]) 
#failed_login()
keypad_gen()
