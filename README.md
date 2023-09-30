# Livestream-PubSub-Protocol
My design and implementation of a protocol for a publish subscribe system 
for live streaming content.

## Header (9 bytes)

Byte 1 = packet type

Bytes 2-4 = producer id

Byte 5 = stream id

Byte 6-9 = frame id (32 bit unsigned int)

## Packet Types

- ANNOUNCE_STREAM     = 0
- ANNOUNCE_STREAM_ACK = 1
- PRODUCE_FRAME       = 2
- SUB_STREAM          = 3 
- SUB_STREAM_ACK      = 4
- UNSUB_STREAM        = 5
- UNSUB_STREAM_ACK    = 6
- SUB_PRODUCER        = 7
- SUB_PRODUCER_ACK    = 8
- UNSUB_PRODUCER      = 9
- UNSUB_PRODUCER_ACK  = 10
- SEND_FRAME          = 11

## Demo 1 IP Addrs / Port

- Port = 50000
- Consumer = 172.20.0.2
- Producer = 172.20.0.3
- Broker = 172.20.0.4


