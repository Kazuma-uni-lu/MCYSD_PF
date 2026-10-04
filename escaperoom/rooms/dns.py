import base64
import codecs

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

    #traverse the file again, only this time pre-checking for the correct hint
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            current_line = line.strip()
            if current_line.startswith("#") or not current_line.startswith("hint" + decrypted_payload):
                continue
            key, value = current_line.split("=", 1)
            key = key.strip()
            value = value.strip()
            print(key, value)
            if current_line.find(":") != -1:
                encoding, payload = value.split(":", 1)
                if encoding == "rot13+b64":
                    #decode rot13
                    rot13_decoded_message = codecs.decode(payload, "rot13")

                    #decode base64
                    decrypted_payload = base64.b64decode(rot13_decoded_message).decode()

                    #remove period at the end and save final word
                    decrypted_payload = decrypted_payload.removesuffix(".")

                    #extracted dns token
                    dns_token = decrypted_payload[decrypted_payload.rfind(" ")+1:]
                    print("Decrypted hint: " + dns_token)
                    

decode("data/dns.cfg")