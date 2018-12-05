import struct
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
    tcp.tcp_close()

    # tokenize the data to extract the identity token and the UDP port
    tokens = tcp_response.split(' ')
    id_token = tokens[1]
    udp_port = tokens[2]

    ''' ****UDP PART**** '''
    udp = udp_class.UDP(host, udp_port)

    # UDP message and packing it in the right structure
    # cid: char[8] , ack: Bool, eom: Bool[8], data_remaining: unsigned short, content_length: unsigned short, content: char[64]
    CID = id_token.encode('utf-8')  # client's id token
    ACK = True  # acknowledgment
    EOM = False
    data_remaining = 0  # length of the data still remaining when using multipart messages
    content = ("Hello from " + id_token + "\r\n").encode('UTF-8')   # message content
    content_length = len(content) # length of the message

    # packing the udp message
    udp_msg = struct.pack('!8s??HH64s', CID, ACK, EOM, data_remaining, content_length, content)

    # get the EOM of the received message and the list of words from the server
    EOM, received_word_list = udp.send_and_receive(udp_msg)
    reversed_words = udp.reversed_words_to_be_sent(received_word_list)
    print(EOM)

    # send the reversed list of words to the server until the last message from the server, i.e, EOM=True
    while (EOM is not True):
        udp_msg = struct.pack('!8s??HH64s', CID, ACK, EOM, data_remaining, len(reversed_words), reversed_words.encode('utf-8'))
        EOM, received_word_list = udp.send_and_receive(udp_msg)
        reversed_words = udp.reversed_words_to_be_sent(received_word_list)
        print(EOM)

    udp.udp_close()

if __name__ == '__main__':
    main()