import base64

def decode(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()
            #ignore comments in the .cfg file
            if current_line.startswith("#"):
                continue
            key, value = current_line.split("=", 1)
            key = key.strip()
            value = value.strip()
            print(key + "=" + value)
            #check to see if the line contains a message to decode
            if current_line.find(":") != -1:
                encoding, payload = value.split(":", 1)
                if key == "token_tag":
                    if encoding == "b64":
                        #decode base64 message to extract the hint
                        decrypted_payload = base64.b64decode(payload).decode()
                        print("The correct hint is number " + decrypted_payload)

                        #transform payload back into utf-8
                        reversed_payload = base64.b64encode(decrypted_payload.encode("utf-8"))
                        reversed_payload_string = reversed_payload.decode("ascii")
                        print("Encoded Base64 before decoding : " + payload)
                        print("Reencoded Base64 message : " + reversed_payload_string )


        
    '''encoded_message.strip()
    print(encoded_message)
    if(encoded_message.find("b64:") != -1):
        new_message = encoded_message[encoded_message.find(":")+1:]
        print(new_message)
        decoded_message = base64.b64decode(new_message).decode()
        print("The correct hint is number " + decoded_message'''

decode("data/dns.cfg")