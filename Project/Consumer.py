from typing import Dict
from ProtocolSocketBase import ProtocolSocketBase

from util import *

class Consumer(ProtocolSocketBase):
    def __init__(self, local_ip: str = "consumer0") -> None:
        super().__init__(local_ip, CONSUMER_PORT)
        self.cons_id = local_ip
        self.subscription_frame_counts: Dict[str, int] = {}
  
    def subscribe_stream(self, prod_id: str, stream_id: str) -> None:
        topic_id = f"{prod_id}{stream_id}"
        print("Subscribing to topic - ", topic_id)

        # send sub packet to broker
        header = {
            HeaderData.PACKET_TYPE: PacketType.SUB_STREAM,
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id
        }
        self._send(header, BROKER_IP, BROKER_PORT)

        print("Subscription packet sent - ", topic_id)

        # receive ACK and highest frame published from Broker
        data = self._receive()[0]
        assert(data[Labels.PACKET_TYPE] == PacketType.SUB_STREAM_ACK.value)
        assert(data[Labels.STREAM_ID] == int(stream_id))

        self.subscription_frame_counts[topic_id] = data[Labels.FRAME_ID]

        print("Reply from Broker - ", data[Labels.BODY])

    def subscribe_producer(self, prod_id: str) -> None:
        pass
    
    def unsubscribe_stream(self, prod_id: str, stream_id: str) -> None:
        pass

    def unsubscribe_producer(self, prod_id: str) -> None:
        pass


        