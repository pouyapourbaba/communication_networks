import socket
import struct

class UDP():
    # class variables
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_and_receive(self, msg):
        # send message to the server via UDP
        self.sock.sendto(msg, (self.ip, int(self.port)))

        # receive the data with a buffer of 1024 bytes
        udp_rsp, sender = self.sock.recvfrom(1024)

        udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)

        # getting the words sent by the server
        words = udp_rsp_unpacked[5]
        words = words.decode('UTF-8')
        # putting the words in an array
        word_list = words.split(' ')

        return word_list

    def reversed_words_to_be_sent(self, list):
        # build the new message to be sent to the server from the reversed words
        list.reverse()
        new_msg = ""
        for i in list:
            new_msg = new_msg + i.rstrip('\0') + ' '
        new_msg = new_msg.strip()

        return new_msg

    # sock.close()