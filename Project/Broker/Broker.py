from typing import Dict
from ProtocolSocketBase import ProtocolSocketBase

from util import *

class Broker(ProtocolSocketBase):
    def __init__(self) -> None:
        super().__init__(BROKER_IP, 50000)
        self.pubs: Dict[str, Dict[int, int]] = {}
        self.subs: Dict[str, Dict[int, int]] = {}
