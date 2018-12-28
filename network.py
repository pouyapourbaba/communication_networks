# importing the required packages
import struct
import tcp_class
import udp_class
import os
import binascii
import argparse

# a function for generating random keys for encryption
def random_keys(n):
    keys = ""
    for i in range(n):
        keys = keys + binascii.b2a_hex(os.urandom(32)).decode("utf-8") + '\r\n'

    return keys

# a function for encrypting the messages
def encryption(content, key):
    content_encrypted = ""
    for i in range(len(content)):
        content_encrypted = content_encrypted + chr(ord(content[i]) ^ ord(key[i]))

    content_encrypted = content_encrypted.encode('UTF-8')

    return content_encrypted

# a function for decrypting the messages
def decryption(data, key):
    decrypted_content = ""
    for i in range(len(data)):

        decrypted_content = decrypted_content + chr(ord(data[i]) ^ ord(key[i]))

    return decrypted_content

# a function for splitting messages into 64bytes in case of multipart messaging
def split64(msg):
    chunk_len = 64
    res = [msg[y - chunk_len:y] for y in range(chunk_len, len(msg) + chunk_len, chunk_len)]

    return res

def main():
    # port = 10000
    # host = '87.92.113.80'


    # parsing the command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True,
                    help="The IP address of the host")
    ap.add_argument("--port", required=True,
                    help="The port number of the host")
    args = vars(ap.parse_args())

    host = args["host"]
    port = int(args["port"])
    # display the host and the port
    print("Host: {}\nPort: {}".format(host, port))

    ''' ****TCP PART**** '''
    # create 20 random keys 64bytes size
    keys_string = random_keys(20)
    client_keys = keys_string.split('\r\n')
    client_keys = client_keys[:-1]

    # construct the message with the features
    message = "HELLO ENC MUL\r\n" + keys_string + ".\r\n"

    # send and receive via TCP protocol
    tcp = tcp_class.TCP(host, port)
    tcp_response = tcp.send_and_receive(message)

    # closing the TCP socket
    tcp.tcp_close()

    # tokenize the data to extract the identity token and the UDP port
    tokens = tcp_response.split(' ')
    id_token = tokens[1]
    udp_port_and_keys = tokens[2].split('\r\n')
    udp_port = udp_port_and_keys[0]

    # extract the keys and store them in a list
    server_keys = []
    for i in range(len(udp_port_and_keys) - 1):
        server_keys.append(udp_port_and_keys[i + 1])

    ''' ****UDP PART**** '''
    # create an object of the "udp_class"
    udp = udp_class.UDP(host, udp_port)

    # UDP message and packing it in the right structure
    # cid: char[8] , ack: Bool, eom: Bool[8], data_remaining: unsigned short, content_length: unsigned short, content: char[64]
    CID = id_token.encode('utf-8')  # client's id token
    ACK = True  # acknowledgment
    EOM = False
    data_remaining = 0  # length of the data still remaining when using multipart messages
    content = ("Hello from " + id_token + "\r\n")  # message content
    # encrypt the content of the message with the first generated keys
    content_encrypted = encryption(content, client_keys[0])
    content_length = len(content) # length of the message

    # packing the udp message
    udp_msg = struct.pack('!8s??HH64s', CID, ACK, EOM, data_remaining, content_length, content_encrypted)

    # send the UDP message using the "send" method provided in the "udp_class"
    udp.send(udp_msg)

    # getting the EOM of the received message and the list of words from the server
    EOM, received_encrypted_words, remaining = udp.receive()

    # splitting the received message into 64 bytes
    chunks = split64(received_encrypted_words)

    # decrypting the data
    decrypted_chunks = ''
    dec_iter = 0
    for chunk in chunks:
        decrypted_chunks += decryption(chunk, server_keys[dec_iter])
        dec_iter += 1

    # reversing the received messages
    reversed_words = udp.reversed_words_to_be_sent(decrypted_chunks.split(' '))

    # sending the reversed list of words to the server until the last message from the server, i.e, EOM=True
    key_index = 1
    while (EOM is not True):
        # splitting the data to be sent into chunks of 64 bytes
        chunks_to_be_encrypted = split64(reversed_words)

        # encrypting the data
        new_msg = []
        for chunk in chunks_to_be_encrypted:
            new_msg.append(encryption(chunk, client_keys[key_index]))
            key_index += 1

        # packing the multipart messages and sending them via UDP
        data_remaining1 = len(reversed_words)
        for msg in new_msg:
            data_remaining1 = data_remaining1 - len(msg)
            udp_msg = struct.pack('!8s??HH64s', CID, ACK, EOM, data_remaining1, len(msg), msg)
            udp.send(udp_msg)

        # receiving the UDP messages
        EOM, received_encrypted_words, remaining = udp.receive()

        # checking to see if the previously received message is the last message from the server or not
        # if not last message
        if EOM is not True:
            # splitting the received message
            chunks1 = split64(received_encrypted_words)
            decrypted_chunks1 = ''

            # decrypting the 64 byte chunks
            for chunk in chunks1:
                decrypted_chunks1 += decryption(chunk, server_keys[dec_iter])
                dec_iter += 1
            reversed_words = udp.reversed_words_to_be_sent(decrypted_chunks1.split(' '))
        # if the last message
        else:
            # print the last message on the terminal
            print(received_encrypted_words)

    # closing the UDP socket
    udp.udp_close()

if __name__ == '__main__':
    main()