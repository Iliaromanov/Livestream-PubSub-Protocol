from typing import Dict
from ProtocolSocketBase import ProtocolSocketBase

from util import *

class Consumer(ProtocolSocketBase):
    def __init__(self, local_ip: str = "consumer0") -> None:
        super().__init__(local_ip, 50000)
        self.subscribed_to: Dict[str, int] = {}
        
        print(f"Consumer - [{local_ip}] - setup complete. Waiting for requests to subscribe ...")

    
    def subscribe_stream(self, stream_id: str) -> None:
        pass

    def subscribe_producer(self, producer_id: str) -> None:
        pass
    
    def unsubscribe_stream(self, stream_id: str) -> None:
        pass

    def unsubscribe_producer(self, producer_id: str) -> None:
        pass


        