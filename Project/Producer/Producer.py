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
        topic_id = self.prod_id + stream_id

    def publish_frame(self, streamID: str, frameID: str) -> None:
        assert(streamID in self.streams)

    


    
