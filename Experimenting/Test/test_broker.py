import socket

LOCAL_IP    = "test-broker"
LOCAL_PORT  = 50000
BUFFER_SIZE = 1024

# Create a UDP socket (UDP cus uses datagram packets)
UDPBrokerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to IP and port (required to recieve data on this socket)
UDPBrokerSocket.bind((LOCAL_IP, LOCAL_PORT))

print("Broker up and listening")

while True:
    print("------ Waiting on message ...")
    msg, sender_addr_port = UDPBrokerSocket.recvfrom(BUFFER_SIZE)

    print("Broker Received Msg: ", msg)
    print("From addr: ", sender_addr_port)

    ack = f"ACK -- broker received: '{msg}'"
    ack_bytes = str.encode(ack)

    UDPBrokerSocket.sendto(ack_bytes, sender_addr_port)
