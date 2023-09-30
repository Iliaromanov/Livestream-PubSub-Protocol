import os
from typing import Dict
from ProtocolSocketBase import ProtocolSocketBase

from util import *

class Producer(ProtocolSocketBase):
    def __init__(self, local_ip: str = "producer0") -> None:
        super().__init__(local_ip, PRODUCER_PORT)
        self.prod_id = os.urandom(3).hex() # random 3 byte string
        self.streams: Dict[str, int] = {}
    
    def publish_new_stream(self, stream_id: str) -> None:
        topic_id = f"{self.prod_id}{stream_id}"
        print(f"Publishing stream {stream_id}. (Topic {topic_id})")
        self.streams[stream_id] = 0 # start at frame 0
        
        # send stream to broker
        header = {
            HeaderData.PACKET_TYPE: PacketType.ANNOUNCE_STREAM,
            HeaderData.PRODUCER_ID: self.prod_id,
            HeaderData.STREAM: stream_id,
        }
        self._send(header, BROKER_IP, BROKER_PORT)

        print("Publish packet sent - ", topic_id)

        # Receive ACK
        data = self._receive()[0]
        assert(data[Labels.PACKET_TYPE] == PacketType.ANNOUNCE_STREAM_ACK.value)
        assert(data[Labels.PRODUCER_ID] == self.prod_id)
        print("Reply from Broker - ", data[Labels.BODY])

    def publish_frame(self, streamID: str, frameID: str) -> None:
        assert(streamID in self.streams)

    


    
