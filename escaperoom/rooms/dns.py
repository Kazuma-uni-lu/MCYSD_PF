import base64
import codecs


from escaperoom.rooms.base import GameState,Room
#dns -> DNS
#soc, dns, vault, malware, final

class DnsRoom(Room):
    def __init__(self, path):
        super().__init__(
            name = "dns",
            description= "You enter the DNS Closet.\nThe walls are covered with scribbled key=value pairs.\nItems here: dns.cfg",
            item = "dns.cfg",
            path = path,
            token_name = "DNS"
        )
    def solve(self, state:GameState):
        dns_token, hintX, encoding, sentence = decode(self.path + "/" + self.item)
        state.tokens["DNS"] = dns_token
        state.inventory.add("DNS")
        return [
            f"TOKEN[{self.token_name}]={dns_token}",
            f"EVIDENCE[{self.token_name}].KEY={hintX}",
            f"EVIDENCE[{self.token_name}].ENCODING={encoding}",
            f"EVIDENCE[{self.token_name}].DECODED_LINE={sentence}",
        ]
def decode(path) -> str:
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()
            #ignore comments in the .cfg file
            if current_line.startswith("#"):
                continue
            key, value = current_line.split("=", 1)
            key = key.strip()
            value = value.strip()
            #print(key + "=" + value)
            #check to see if the line contains a message to decode
            if current_line.find(":") != -1:
                encoding, payload = value.split(":", 1)
                if key == "token_tag":
                    if encoding == "b64":
                        #decode base64 message to extract the hint
                        decrypted_payload = base64.b64decode(payload).decode()
                        #print("The correct hint is number " + decrypted_payload)

                        #transform payload back into utf-8
                        reversed_payload = base64.b64encode(decrypted_payload.encode("utf-8"))
                        reversed_payload_string = reversed_payload.decode("ascii")
                        #print("Encoded Base64 before decoding : " + payload)
                        #print("Reencoded Base64 message : " + reversed_payload_string )
                    elif encoding == "rot13+b64":
                        #decode rot13 first
                        rot13_decoded_message = codecs.decode(payload, "rot13")

                        decrypted_payload = base64.b64decode(rot13_decoded_message).decode()
                        reversed_payload = base64.b64encode(decrypted_payload.encode("utf-8"))
                        reversed_payload_string = reversed_payload.decode("ascii")
                    else:
                        return [
                            f"Encoding not valid.",
                            f"Token could not be read!"
                        ]


    #traverse the file again, only this time pre-checking for the correct hint
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()
            if current_line.startswith("#") or not current_line.startswith("hint" + decrypted_payload):
                continue
            key, value = current_line.split("=", 1)
            key = key.strip()
            value = value.strip()
            #print(key, value)
            if current_line.find(":") != -1:
                encoding, payload = value.split(":", 1)
                if encoding == "rot13+b64":
                    #decode rot13
                    rot13_decoded_message = codecs.decode(payload, "rot13")

                    #decode base64
                    sentence = base64.b64decode(rot13_decoded_message).decode()

                    #remove period at the end and save final word
                    decrypted_payload = sentence.removesuffix(".")

                    #extracted dns token
                    dns_token = decrypted_payload[decrypted_payload.rfind(" ")+1:]
                    #print("Decrypted hint: " + dns_token)
                    return dns_token, key, encoding, sentence
                elif encoding == "b64":
                    sentence = base64.b64decode(rot13_decoded_message).decode()

                    decrypted_payload = sentence.removesuffix(".")

                    dns_token = decrypted_payload[decrypted_payload.rfind(" ")+1:]

                    return dns_token, key, encoding, sentence
                else:
                        return [
                            f"Encoding not valid.",
                            f"Hint could not be extracted!"
                        ]

                    

#print(decode("data/dns.cfg"))
if __name__ == "__main__":
    state = GameState()
    room = DnsRoom("data")

    for line in room.solve(state):
        print(line)

    print(state.tokens)
    print(state.inventory)