from enum import Enum, auto


# Constants
BROKER_IP       = "broker"
BROKER_PORT     = 50000
PRODUCER_PORT   = 50000
CONSUMER_PORT   = 50000
DEFAULT_PROD_ID = '000000'
BUFFER_SIZE     = 1024 # not sure if should change this or not


class PacketType(Enum):
    ANNOUNCE_STREAM     = 0
    ANNOUNCE_STREAM_ACK = 1
    PRODUCE_FRAME       = 2
    SUB_STREAM          = 3 
    SUB_STREAM_ACK      = 4
    UNSUB_STREAM        = 5
    UNSUB_STREAM_ACK    = 6
    SUB_PRODUCER        = 7
    SUB_PRODUCER_ACK    = 8
    UNSUB_PRODUCER      = 9
    UNSUB_PRODUCER_ACK  = 10
    SEND_FRAME          = 11


class HeaderData(Enum):
    PACKET_TYPE = auto()
    PRODUCER_ID = auto()
    STREAM      = auto()
    FRAME       = auto()


class Commands(Enum):
    PUB    = "pub"
    STREAM = "stream"
    SUB    = "sub"
    UNSUB  = "unsub"
    EXIT   = "exit"


class Labels(Enum):
    # for unpacking header dict
    PACKET_TYPE = "packet_type"
    PRODUCER_ID = "producer_id"
    STREAM_ID   = "stream_id"
    FRAME_ID    = "frame_id"
    BODY        = "body"

    # for Broker dict keys
    SUBS        = "subs"
    FRAME_COUNT = "frame_count"
