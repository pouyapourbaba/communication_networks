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

# a function for splitting messages into 64bytes
def split64(msg):
    chunk_len = 64
    res = [msg[y - chunk_len:y] for y in range(chunk_len, len(msg) + chunk_len, chunk_len)]

    return res

def main():
    host = '87.92.113.80'
    port = 10000

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
    udp.send(udp_msg)

    EOM, received_encrypted_words, remaining = udp.receive()
    re = remaining
    # decrypt the data
    chunks = split64(received_encrypted_words)
    decrypted_chunks = ''
    dec_iter = 0
    for chunk in chunks:
        decrypted_chunks += decryption(chunk, server_keys[dec_iter])
        dec_iter += 1
    #print(decrypted_chunks)

    reversed_words = udp.reversed_words_to_be_sent(decrypted_chunks.split(' '))

    # send the reversed list of words to the server until the last message from the server, i.e, EOM=True
    key_index = 1
    while (EOM is not True):
        chunks_to_be_encrypted = split64(reversed_words)
        new_msg = []
        for chunk in chunks_to_be_encrypted:
            new_msg.append(encryption(chunk, client_keys[key_index]))
            key_index += 1
        #print('new message')
        #print(new_msg)

        data_remaining1 = len(reversed_words)
        for msg in new_msg:
            data_remaining1 = data_remaining1 - len(msg)
            udp_msg = struct.pack('!8s??HH64s', CID, ACK, EOM, data_remaining1, len(msg), msg)
            udp.send(udp_msg)

        EOM, received_encrypted_words, remaining = udp.receive()

        if EOM is not True:
            chunks1 = split64(received_encrypted_words)
            decrypted_chunks1 = ''

            for chunk in chunks1:
                decrypted_chunks1 += decryption(chunk, server_keys[dec_iter])
                #print(decrypted_chunks1)
                #print(server_keys[dec_iter])
                dec_iter += 1
                print(dec_iter)
            #print('the whole message to be sent')
            #print(decrypted_chunks1)
            #print(dec_iter)
            reversed_words = udp.reversed_words_to_be_sent(decrypted_chunks1.split(' '))
            #print('still sending')
        else:
            print('done')
            print(received_encrypted_words)

    # print(dec_iter)

    udp.udp_close()

if __name__ == '__main__':
    main()