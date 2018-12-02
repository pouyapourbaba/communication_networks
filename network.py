import struct
import sys

# import the classes
import tcp_class
import udp_class

def main():

    host = '87.92.113.80'
    port = 10000

    ''' ****TCP PART**** '''
    # send and receive via TCP protocol
    tcp = tcp_class.TCP(host, port)
    tcp_sock = tcp.sock_connect()
    tcp.send("HELLO\r\n")
    tcp_rsp = tcp.receive()

    # tokenize the data to extract the identity token and the UDP port
    tokens = tcp_rsp.split(' ')
    id_token = tokens[1]
    udp_port = tokens[2]

    tcp_sock.close()


    ''' ****UDP PART**** '''
    # initialize the UDP socket
    udp = udp_class.UDP(host, udp_port)
    udp_sock = udp.sock_connect()


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
    # sending the udp message to the server
    udp.send(udp_msg)

    # receive the data from the server
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    print(udp_rsp_unpacked)

    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 1st time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 2nd time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 3rd time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 4th time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 5th time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 6th time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 7th time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    ''' ****Send the reveres words back to the server 8th time**** '''
    new_msg = udp.new_msg(reversed_words)
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
    udp.send(udp_msg)
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    reversed_words = udp.reverse(udp_rsp_unpacked)
    print(reversed_words)

    udp_sock.close()


if __name__ == '__main__':
    main()