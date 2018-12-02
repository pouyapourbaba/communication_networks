import socket

class TCP():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # initialize the TCP socket and connect to the given ip address and port number
    def sock_con(self):
        self.sock = socket.socket()
        self.sock.connect((self.ip, self.port))
        return self.sock

    # send message to the server via TCP, in byte strings
    def send(self, msg):
        self.msg = msg.encode('UTF-8')
        self.sock.send(self.msg)

    # receive the data with a buffer of 1024 bytes
    def receive(self):
        tcp_rsp = self.sock.recv(1024)
        tcp_rsp = tcp_rsp.decode('UTF-8')
        return tcp_rsp

    
