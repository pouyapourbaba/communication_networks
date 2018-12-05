import socket
import struct
import sys
import tcp_class
import udp_class


def main():
    host = '87.92.113.80'
    port = 10000

    ''' ****TCP PART**** '''
    message = "HELLO\r\n"

    # send and receive via TCP protocol
    tcp = tcp_class.TCP(host, port)
    tcp_response = tcp.send_and_receive(message)

    # tokenize the data to extract the identity token and the UDP port
    tokens = tcp_response.split(' ')
    id_token = tokens[1]
    udp_port = tokens[2]


    ''' ****UDP PART**** '''

    udp = udp_class.UDP(host, udp_port)

    # UDP message and packing it in the right structure
    # cid: char[8] , ack: Bool, eom: Bool[8], data_remaining: unsigned short, content_length: unsigned short, content: char[64]
    cid = id_token.encode('utf-8')  # client's id token
    ack = True  # acknowledgment
    eom = False
    data_remaining = 0  # length of the data still remaining when using multipart messages
    content = ("Hello from " + id_token + "\r\n").encode('UTF-8')   # message content
    content_length = len(content) # length of the message

    # packing the udp message
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, content_length, content)

    received_word_list = udp.send_and_receive(udp_msg)
    print(received_word_list)
    reversed_words = udp.reversed_words_to_be_sent(received_word_list)
    print(reversed_words)

    # udp = udp_class.UDP(host, udp_port)
    # udp_sock = udp.sock_connect()
    ''' ****Send the reveres words back to the server 1st time**** '''
    # new_msg = udp.new_msg(reversed_words)

    while received_word_list[0] != 'You' and received_word_list[1] != 'replied':
        udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(reversed_words), reversed_words.encode('utf-8'))
        received_word_list = udp.send_and_receive(udp_msg)
        print(received_word_list)
        reversed_words = udp.reversed_words_to_be_sent(received_word_list)
        print(reversed_words)

    # udp_sock.close()


if __name__ == '__main__':
    main()