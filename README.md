# Livestream-PubSub-Protocol
My design and implementation of a protocol for a publish subscribe system 
for live streaming content.

## Header (13 bytes)

```
Byte 1     = packet type
Bytes 2-4  = producer id
Byte 5     = stream id
Byte 6-9   = frame id (32 bit unsigned int)
Byte 10-13 = text id (32 bit unsigned int)
```

## Packet Types

```
- ANNOUNCE_STREAM     = 0
- ANNOUNCE_STREAM_ACK = 1
- SEND_FRAME          = 2 # can be used for both prod send to broker, and broker send to cons
- SEND_TEXT           = 3 # can be used for both prod send to broker, and broker send to cons
- SUB_STREAM          = 4 
- SUB_STREAM_ACK      = 5
- UNSUB_STREAM        = 6
- UNSUB_STREAM_ACK    = 7
- SUB_PRODUCER        = 8
- SUB_PRODUCER_ACK    = 9
- UNSUB_PRODUCER      = 10
- UNSUB_PRODUCER_ACK  = 11
```


## Demo 2 IP Addresses
```
Producer0 = 172.17.0.2
Producer1 = 172.17.0.6
Consumer0 = 172.17.0.4
Consumer1 = 172.17.0.5
Broker    = 172.17.0.3
```

<!-- ## Demo 1 IP Addrs / Port

- Port = 50000
- Consumer = 172.20.0.2
- Producer = 172.20.0.3
- Broker = 172.20.0.4 -->


