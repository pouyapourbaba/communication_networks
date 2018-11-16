import socket
import sys

def main():

    # use the command line args to get the server ip and port
    if len(sys.argv) > 2:
        host = sys.argv[1]
        port = sys.argv[2]
        port = int(port)

    # initialize the TCP socket
    sock_tcp = socket.socket()
    sock_tcp.connect((host, port))

    # message to be sent to the server via TCP, in byte strings
    message_tcp = 'HELLO\r\n'
    message_tcp = message_tcp.encode('UTF-8')
    sock_tcp.send(message_tcp)

    # receive the data with a buffer of 1024 bytes
    response_tcp = sock_tcp.recv(1024)
    response_tcp = response_tcp.decode('UTF-8')

    # tokenize the data to extract the identity token and the UDP port
    tokens = response_tcp.split(' ')
    id_token = tokens[1]
    udp_port = tokens[2]

    sock_tcp.close()


    # initialize the UDP socket
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, int(udp_port))
    print(server_address)

    # UDP message
    message_udp = "Hello from " + id_token + "\r\n"
    message_udp = message_udp.encode('UTF-8')
    socket_udp.sendto(message_udp, server_address)

    # receive data
    response_udp, server = socket_udp.recvfrom(4096)

    socket_udp.close()

if __name__ == '__main__':
    main()