import base64

encoded_message = "token_tag=b64:NA=="

def decode():
    encoded_message.strip()
    print(encoded_message)
    if(encoded_message.find("b64:") != -1):
        new_message = encoded_message[encoded_message.find(":")+1:]
        print(new_message)
        decoded_message = base64.b64decode(new_message).decode()
        print(decoded_message)

decode()