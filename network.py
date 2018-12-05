import struct
import tcp_class
import udp_class
import os
import binascii

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

# a function for decryption
def decryption(data, key):
    decrypted_content = ""
    for i in range(len(data)):
        decrypted_content = decrypted_content + chr(ord(data[i]) ^ ord(key[i]))

    return decrypted_content

def main():
    host = '87.92.113.80'
    port = 10000

    ''' ****TCP PART**** '''
    # create 20 random keys 64bytes size
    keys_string = random_keys(20)
    client_keys = keys_string.split('\r\n')

    # construct the message with the features
    message = "HELLO ENC\r\n" + keys_string + ".\r\n"

    # send and receive via TCP protocol
    tcp = tcp_class.TCP(host, port)
    tcp_response = tcp.send_and_receive(message)
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

    # get the EOM of the received message and the list of words from the server
    EOM, received_encrypted_words = udp.send_and_receive(udp_msg)
    # decrypt the data
    #print(received_word_list)
    received_decrypted_words = decryption(received_encrypted_words, server_keys[0])
    print(received_decrypted_words)
    reversed_words = udp.reversed_words_to_be_sent(received_decrypted_words.split(' '))
    #print(reversed_words)
    # send the reversed list of words to the server until the last message from the server, i.e, EOM=True
    key_index = 1
    while (EOM is not True):
        new_msg = encryption(reversed_words, client_keys[key_index])
        udp_msg = struct.pack('!8s??HH64s', CID, ACK, EOM, data_remaining, len(reversed_words), new_msg)
        EOM, received_encrypted_words= udp.send_and_receive(udp_msg)
        if EOM is not True:
            received_decrypted_words = decryption(received_encrypted_words, server_keys[key_index])
            print(received_decrypted_words)
        else:
            print(received_encrypted_words)
        reversed_words = udp.reversed_words_to_be_sent(received_decrypted_words.split(' '))
        #print(reversed_words)

        key_index = key_index + 1

    udp.udp_close()

if __name__ == '__main__':
    main()