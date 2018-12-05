import socket

class TCP():

    # class variables
    sock = socket.socket()

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_and_receive(self, msg):
        # send message to the server via TCP, in byte strings
        self.sock.connect((self.ip, self.port))
        msg = msg.encode('UTF-8')
        self.sock.send(msg)

        # receive the data with a buffer of 1024 bytes
        tcp_rsp = self.sock.recv(1024)
        tcp_rsp = tcp_rsp.decode('UTF-8')

        self.sock.close()

        return tcp_rsp