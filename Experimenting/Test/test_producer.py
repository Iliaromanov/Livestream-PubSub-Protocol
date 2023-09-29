import socket


LOCAL_IP    = "test-producer"
LOCAL_PORT  = 50000
BROKER_IP   = "test-broker"
BROKER_PORT = 50000
BUFFER_SIZE = 1024

UDPProducerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPProducerSocket.bind((LOCAL_IP, LOCAL_PORT))

print("Producer setup complete. Sending Message.")

while True:
    msg = "PROD: " + input()
    msg_byte = str.encode(msg)

    UDPProducerSocket.sendto(msg_byte, (BROKER_IP, BROKER_PORT))

    print("Msg sent to broker")

    msg_received, addr = UDPProducerSocket.recvfrom(BUFFER_SIZE)

    print("Msg received from broker:", msg_received)
    print("Broker Addr: ", addr)


    print("--- END OF PRODUCER ---")

