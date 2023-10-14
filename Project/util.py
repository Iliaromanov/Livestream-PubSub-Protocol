from enum import Enum, auto
import os

# Constants
BROKER_IP             = "broker"
BROKER_PORT           = 50000
PRODUCER_PORT         = 50000
CONSUMER_PORT         = 50000
CONSUMER_CONTENT_PORT = 50001
DEFAULT_PROD_ID       = '000000'
BUFFER_SIZE           = 1024 # not sure if should change this or not


def file_to_bytes(path: str) -> bytearray:
    with open(path, 'rb') as img_file:
        return bytearray(img_file.read())
    
def text_file_to_bytes(path: str) -> bytearray:
    with open(path, 'r') as text_file:
        text = text_file.read()
        return bytearray(text.encode())

    
def bytes_to_frame(frame_bytes: bytearray, topic_id: str) -> None:
    # saves to a file locally????
    pass


class PacketType(Enum):
    ANNOUNCE_STREAM     = 0
    ANNOUNCE_STREAM_ACK = 1
    SEND_FRAME          = 2 # can be used for both prod -> broker, and broker -> cons
    SEND_TEXT           = 3 # can be used for both prod -> broker, and broker -> cons
    SUB_STREAM          = 4 
    SUB_STREAM_ACK      = 5
    UNSUB_STREAM        = 6
    UNSUB_STREAM_ACK    = 7
    SUB_PRODUCER        = 8
    SUB_PRODUCER_ACK    = 9
    UNSUB_PRODUCER      = 10
    UNSUB_PRODUCER_ACK  = 11


class HeaderData(Enum):
    PACKET_TYPE = auto()
    PRODUCER_ID = auto()
    STREAM      = auto()
    FRAME       = auto()
    TEXT        = auto()


class Commands(Enum):
    PUB    = "pub"    # announce new stream
    STREAM = "stream" # send frame to broker
    SUB    = "sub"
    UNSUB  = "unsub"
    EXIT   = "exit"


class Labels(Enum):
    # for unpacking header dict
    PACKET_TYPE = "packet_type"
    PRODUCER_ID = "producer_id"
    STREAM_ID   = "stream_id"
    FRAME_ID    = "frame_id"
    TEXT_ID     = "text_id"
    BODY        = "body"

    # for Broker dict keys
    SUBS        = "subs"
    FRAME_COUNT = "frame_count"
    TEXT_COUNT  = "text_count"
