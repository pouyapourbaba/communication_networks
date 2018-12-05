import struct
import os
import binascii

# import the classes
import tcp_class
import udp_class

def main():

    host = '87.92.113.80'
    port = 10000

    ''' ****TCP PART**** '''
    # create 20 random keys 64bytes size
    keys =""
    for i in range(20):
         keys = keys + binascii.b2a_hex(os.urandom(32)).decode("utf-8") + '\r\n'

    client_keys = keys.split('\r\n')

    # send and receive via TCP protocol
    tcp = tcp_class.TCP(host, port)
    tcp_sock = tcp.sock_connect()
    tcp.send("HELLO ENC\r\n" + keys + ".\r\n")
    tcp_rsp = tcp.receive()

    # tokenize the data to extract the identity token and the UDP port and the encryption keys
    tokens = tcp_rsp.split(' ')
    # the id token received from the server
    id_token = tokens[1]
    # the token that contains the udp port and the encryption keys
    udp_port_and_keys = tokens[2].split('\r\n')
    udp_port = udp_port_and_keys[0]
    # extract the keys and store them in a list
    server_keys = []
    for i in range(len(udp_port_and_keys)-1):
        server_keys.append(udp_port_and_keys[i+1])

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
    # content = ("Hello from " + id_token + "\r\n").encode('UTF-8')   # message content
    content = ("Hello from " + id_token + "\r\n")
    content_enc = ""
    for i in range(len(content)):
        content_enc = content_enc + chr(ord(content[i]) ^ ord(client_keys[0][i]))
    # print(content_enc)
    content_length = len(content) # length of the message

    # packing the udp message
    udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, content_length, content_enc.encode('utf-8'))
    # sending the udp message to the server
    udp.send(udp_msg)

    # receive the data from the server
    udp_rsp = udp.receive()
    udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
    # print(udp_rsp_unpacked)

    # decrypt received messages
    data = udp_rsp_unpacked[5]
    data = data.decode('utf-8')
    print(len(data))
    decrypted = ""
    for i in range(len(data)):
        decrypted = decrypted + chr(ord(data[i]) ^ ord(server_keys[0][i]))
    print(decrypted)
    print(len(decrypted))
    reversed_words = udp.reverse(decrypted)
    print(reversed_words)

   #  ''' ****Send the reveres words back to the server 1st time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  ''' ****Send the reveres words back to the server 2nd time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  ''' ****Send the reveres words back to the server 3rd time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  ''' ****Send the reveres words back to the server 4th time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  ''' ****Send the reveres words back to the server 5th time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  ''' ****Send the reveres words back to the server 6th time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  ''' ****Send the reveres words back to the server 7th time**** '''
   #  new_msg = udp.new_msg(reversed_words)
   #  udp_msg = struct.pack('!8s??HH64s', cid, ack, eom, data_remaining, len(new_msg), new_msg.encode('utf-8'))
   #  udp.send(udp_msg)
   #  udp_rsp = udp.receive()
   #  udp_rsp_unpacked = struct.unpack('8s??HH64s', udp_rsp)
   #  print(udp_rsp_unpacked)
   #  #reversed_words = udp.reverse(udp_rsp_unpacked)
   #  #print(reversed_words)
   #
   #  udp_sock.close()


if __name__ == '__main__':
    main()