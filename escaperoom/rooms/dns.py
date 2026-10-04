import base64

def decode(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()
            if current_line.startswith("#") or current_line.find(":") == -1:
                continue
            key, value = current_line.split("=", 1)
            key = key.strip()
            value = value.strip()
            print(key + "=" + value)
            encoding, payload = value.split(":", 1)
            print(encoding, payload)

        
    '''encoded_message.strip()
    print(encoded_message)
    if(encoded_message.find("b64:") != -1):
        new_message = encoded_message[encoded_message.find(":")+1:]
        print(new_message)
        decoded_message = base64.b64decode(new_message).decode()
        print("The correct hint is number " + decoded_message'''

decode("data/dns.cfg")