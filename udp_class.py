import socket

class UDP():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # initialize the UDP socket and connect to the given ip address and port number
    def sock_connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self.sock

    # send message to the server via UDP
    def send(self, msg):
        self.sock.sendto(msg, (self.ip, int(self.port)))

    # receive the data with a buffer of 1024 bytes
    def receive(self):
        udp_rsp, sender = self.sock.recvfrom(1024)
        return udp_rsp

    # reverse the order of the words in the list
    def reverse(self, data):
        # getting the words sent by the server
        # words = data[5]
        # words = words.decode('UTF-8')
        # putting the words in an array
        word_list = data.split(' ')
        # print("from udp_class ")
        # print(word_list)
        # reversing the list of the words
        word_list.reverse()
        return word_list

    # build the new message to be sent to the server from the reversed words
    def new_msg(self, reversed_list):
        new_msg = ""
        for i in reversed_list:
            new_msg = new_msg + i.rstrip('\0') + ' '
        new_msg = new_msg.strip()
        return new_msg