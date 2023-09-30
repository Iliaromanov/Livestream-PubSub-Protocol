from typing import Dict, Set, Any
from ProtocolSocketBase import ProtocolSocketBase

from util import *

class Broker(ProtocolSocketBase):
    def __init__(self) -> None:
        super().__init__(BROKER_IP, BROKER_PORT)
        # {topic_id: {"subs": set(consumer_ip), "frame_count": highest_frame_num}}
        self.topic_info: Dict[str, Dict[str, Any]] = {}
        
        # {prod_id: set(consumer_ip)}
        self.producer_subs: Dict[str, Set[str]] = {}

    def listen(self, buffer_size: int = BUFFER_SIZE) -> None:
        while True:
            print("Broker listening for incoming traffic ...")
            result, addr = self._receive(buffer_size)

            print("Broker received packet from - ", addr)

            packet_type = result[Labels.PACKET_TYPE]
            prod_id = result[Labels.PRODUCER_ID]
            stream_id = result[Labels.STREAM_ID]
            frame_id = result[Labels.FRAME_ID]
            body = result[Labels.BODY]

            if packet_type == PacketType.ANNOUNCE_STREAM.value:
                self.publish_stream(prod_id, stream_id)
            elif packet_type == PacketType.PRODUCE_FRAME.value:
                self.send_frame_to_subs(prod_id, stream_id, frame_id, body)
            elif packet_type == PacketType.SUB_STREAM:
                self.sub_to_stream(addr[0], stream_id)
            elif packet_type == PacketType.UNSUB_STREAM:
                self.unsub_from_stream(addr[0], stream_id)
            elif packet_type == PacketType.SUB_PRODUCER:
                self.sub_to_prod(addr[0], prod_id)
            elif packet_type == PacketType.UNSUB_PRODUCER:
                self.unsub_from_prod(addr[0], prod_id)
            else:
                raise Exception(f"Invalid packet type received by broker - {packet_type}")

    def publish_stream(self, prod_id: str, stream_id: str, prod_ip: str) -> None:
        topic_id = f"{prod_id}{stream_id}"
        print("Publishing new stream topic - ", topic_id)
        
        if prod_id not in self.producer_subs:
            # new producer with no subscribers
            self.producer_subs[prod_id] = set()

        # new topic (since always new stream in this method)
        self.topic_info[topic_id] = {
            Labels.SUBS: set(),
            Labels.FRAME_COUNT: 0
        }

        # ensure that consumers subscribed directly to this producer
        #  are also added to the subscriptions list of this new stream
        for consumer_ip in self.producer_subs[prod_id]:
            self.topic_info[Labels.SUBS].add(consumer_ip)

        # send an ACK
        header = {
            HeaderData.PACKET_TYPE: PacketType.ANNOUNCE_STREAM_ACK.value,
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id
        }
        msg = bytearray(f"ACK - Broker published stream {stream_id}".encode())
        self._send(header, msg, prod_ip, PRODUCER_PORT)

    def send_frame_to_subs(
            self, prod_id: str, stream_id: str,
            frame_id: int, frame: bytes
    ) -> None:
        topic_id = f"{prod_id}{stream_id}"
        print(f"Broker received frame {frame_id} for topic - {topic_id}")

        # update highest_frame in frame counts dict

        for consumer_ip in self.topic_info[topic_id][Labels.SUBS]:
            # will need to use CONSUMER_PORT
            pass

    def sub_to_stream(self, cons_id: str, stream_id: str) -> None:
        pass

    def sub_to_prod(self, cons_id: str, prod_id: str) -> None:
        pass

    def unsub_from_stream(self, cons_id: str, stream_id: str) -> None:
        pass

    def unsub_from_prod(self, cons_id: str, prod_id: str) -> None:
        pass 
    