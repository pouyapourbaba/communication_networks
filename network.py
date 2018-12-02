import socket
import struct
import sys

def main():

    host = '87.92.113.80'
    port = 10000

    # initialize the TCP socket
    tcp_sock = socket.socket()
    tcp_sock.connect((host, port))

    # message to be sent to the server via TCP, in byte strings
    tcp_msg = 'HELLO\r\n'
    tcp_msg = tcp_msg.encode('UTF-8')
    tcp_sock.send(tcp_msg)

    # receive the data with a buffer of 1024 bytes
    tcp_rsp = tcp_sock.recv(1024)
    tcp_rsp = tcp_rsp.decode('UTF-8')

    # tokenize the data to extract the identity token and the UDP port
    tokens = tcp_rsp.split(' ')
    id_token = tokens[1]
    udp_port = tokens[2]

    tcp_sock.close()


    # initialize the UDP socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, int(udp_port))

    # UDP message and packing it in the right structure
    # cid: char[8] , ack: Bool, eom: Bool[8], data_remaining: unsigned short, content_length: unsigned short, content: char[64]

    # client's id token
    cid = id_token
    # acknowledgment
    ack = True
    eom = False
    # length of the data still remaining when using multipart messages
    data_remaining = 0
    # message content
    content = ("Hello from " + id_token + "\r\n").encode('UTF-8')
    # length of the message
    content_length = len(content)

    # packing the udp message and sending it to the server
    udp_msg = struct.pack('!8s??HH64s', cid.encode('utf-8'), ack, eom, data_remaining, content_length, content)
    udp_sock.sendto(udp_msg, server_address)

    # receive the data with a buffer of 1024 bytes
    udp_rsp, sender = udp_sock.recvfrom(1024)
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)

    # getting the words sent by the server
    words = udp_rsp_unpacked[5]
    words = words.decode('UTF-8')
    print(words)
    # putting the words in an array
    word_list = words.split(' ')
    print(word_list)

    # reversing the list of the words
    word_list.reverse()
    print(word_list)

    new_msg = ""
    for i in word_list:
        new_msg = new_msg + i.rstrip('\0') + ' '
    new_msg = new_msg.strip()
    print(word_list[0])
    print(len(word_list[0].rstrip('\0')))

    # sending the words in reverse order
    udp_msg = struct.pack('!8s??HH64s', cid.encode('utf-8'), ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp_sock.sendto(udp_msg, server_address)
    # receive the data with a buffer of 1024 bytes
    udp_rsp, sender = udp_sock.recvfrom(1024)
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)

    print(udp_rsp_unpacked)
    udp_sock.close()


if __name__ == '__main__':
    main()