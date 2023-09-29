import os
from typing import Dict
from ProtocolSocketBase import ProtocolSocketBase

from util import *

class Producer(ProtocolSocketBase):
    def __init__(self, prod_id: str, streams: Dict[str, int], local_ip: str = "producer0") -> None:
        super().__init__(local_ip, 50000)
        
        self.prod_id = os.urandom(3).hex() # random 3 byte string
        self.streams = {}

        print(f"ProducerID - [{self.prod_id}] - setup complete. Waiting for requests to stream.")
    

    def publish_new_stream(self, streamID: int) -> None:
        pass

    def publish_frame(self, streamID: int, frameID: int) -> None:
        assert(streamID in self.streams)

    


    
