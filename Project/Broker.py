from typing import Dict, Set, Any

from ProtocolSocketBase import ProtocolSocketBase
from util import *

class Broker(ProtocolSocketBase):
    def __init__(self) -> None:
        super().__init__(BROKER_IP, BROKER_PORT)
        # {topic_id: {
        #   "subs": set(consumer_ip), 
        #   "frame_count": highest_frame_num, # * highest frame that broker received *
        #   "text_count": highest_text_count} # * highest text that broker received *
        #  (broker will do check for highest count for itself, then each consumer will do its own)
        # }
        self.topic_info: Dict[str, Dict[str, Any]] = {}
        
        # {prod_id: set(consumer_ip)}
        self.producer_subs: Dict[str, Set[str]] = {}

    def listen(self, buffer_size: int = BUFFER_SIZE) -> None:
        while True:
            print("Broker listening for incoming traffic ...")
            try:
                result, addr = self._receive(buffer_size)
            except ProtocolSocketBase.TIMEOUT_EXCEPTION:
                continue

            print("Broker received packet from - ", addr)

            packet_type = result[Labels.PACKET_TYPE]
            prod_id = result[Labels.PRODUCER_ID]
            stream_id = result[Labels.STREAM_ID]
            frame_id = result[Labels.FRAME_ID]
            text_id = result[Labels.TEXT_ID]
            body = result[Labels.BODY]

            if packet_type == PacketType.ANNOUNCE_STREAM.value:
                self.publish_stream(prod_id, stream_id, addr[0])
            elif packet_type == PacketType.SUB_STREAM.value:
                self.sub_to_stream(addr[0], prod_id, stream_id)
            elif packet_type == PacketType.SEND_FRAME.value:
                self.send_content_to_subs(prod_id, stream_id, frame_id, body, True)
            elif packet_type == PacketType.SEND_TEXT.value:
                self.send_content_to_subs(prod_id, stream_id, text_id, body.encode(), False)
            elif packet_type == PacketType.UNSUB_STREAM.value:
                self.unsub_from_stream(addr[0], prod_id, stream_id)
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
            Labels.FRAME_COUNT: -1,
            Labels.TEXT_COUNT: -1
        }

        # ensure that consumers subscribed directly to this producer
        #  are also added to the subscriptions list of this new stream
        for consumer_ip in self.producer_subs[prod_id]:
            self.topic_info[Labels.SUBS].add(consumer_ip)

        # send an ACK
        header = {
            HeaderData.PACKET_TYPE: PacketType.ANNOUNCE_STREAM_ACK,
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id
        }
        msg = bytearray(f"ACK: Broker published stream {stream_id}".encode())
        self._send(
            header_data=header, payload=msg,
            target_ip=prod_ip, target_port=PRODUCER_PORT
        )
        
        print("Publish finished - ", topic_id)

    def sub_to_stream(self, cons_id: str, prod_id: str, stream_id: str) -> None:
        print(f"Sub request from '{cons_id}' to producer '{prod_id}', stream '{stream_id}")
        topic_id = f"{prod_id}{stream_id}"
        if topic_id not in self.topic_info:
            print(f"-- TOPIC {topic_id} DOES NOT EXIST. SUB REQUEST FAIL.")

        self.topic_info[topic_id][Labels.SUBS].add(cons_id)

        highest_published_frame = self.topic_info[topic_id][Labels.FRAME_COUNT]
        highest_published_text = self.topic_info[topic_id][Labels.TEXT_COUNT]

        header = {
            HeaderData.PACKET_TYPE: PacketType.SUB_STREAM_ACK,
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id,
            HeaderData.FRAME: highest_published_frame, # use this to set the max_frame for stream in consumer
            HeaderData.TEXT: highest_published_text
        }
        msg = bytearray(f"ACK: Broker registered sub to topic {topic_id}".encode())
        self._send(
            header_data=header, payload=msg, 
            target_ip=cons_id, target_port=CONSUMER_PORT
        )
        
        print("Sub request completed - ", topic_id)


    def send_content_to_subs(
            self, prod_id: str, stream_id: str,
            content_id: int, content: bytes, is_frame: bool
    ) -> None:
        topic_id = f"{prod_id}{stream_id}"
        print(f"Broker received {'frame' if is_frame else 'text'} {content_id} for topic - {topic_id}")

        header = {
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id,
        }

        # check if already saw a future/the same frame or text
        topic = self.topic_info[topic_id]
        cur_highest = topic[Labels.FRAME_COUNT] if is_frame else topic[Labels.TEXT_COUNT]
        if cur_highest >= content_id:
            print(f"-- Seen a frame/text >= {content_id}; not sending --")
            return

        if is_frame:
            # update cur_highest frame count
            self.topic_info[topic_id][Labels.FRAME_COUNT] = content_id

            header[HeaderData.PACKET_TYPE] = PacketType.SEND_FRAME
            header[HeaderData.FRAME] = content_id
        else:            
            # update cur_highest text count
            self.topic_info[topic_id][Labels.TEXT_COUNT] = content_id

            header[HeaderData.PACKET_TYPE] = PacketType.SEND_TEXT
            header[HeaderData.TEXT] = content_id
        
        # send to all subbed consumers
        for consumer_ip in self.topic_info[topic_id][Labels.SUBS]:
            self._send(header, consumer_ip, CONSUMER_CONTENT_PORT, content)
            print(f"-- Sent {'frame' if is_frame else 'text'} {content_id}, topic {topic_id} to {consumer_ip} --")
            # Don't need ACK because check comment under self.topic in __init__


    def unsub_from_stream(
            self, cons_ip: str, prod_id: str, stream_id: str
    ) -> None:
        topic_id = f"{prod_id}{stream_id}"

        if topic_id not in self.topic_info:
            print(f"-- Topic {topic_id} doesn't exist; can't unsubscribe--")
            return

        # remove from topic's subscriber set
        self.topic_info[topic_id][Labels.SUBS].remove(cons_ip)

        # send ACK
        header = {
            HeaderData.PACKET_TYPE: PacketType.UNSUB_STREAM_ACK,
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id,
        }
        msg = bytearray(f"ACK: Broker unsubbed from topic {topic_id}".encode())
        self._send(
            header_data=header, payload=msg, 
            target_ip=cons_ip, target_port=CONSUMER_PORT
        )
        
        print("-- Unsub request completed - ", topic_id, " --")


    def sub_to_prod(self, cons_id: str, prod_id: str) -> None:
        print(f"Sub request from '{cons_id}' to producer '{prod_id}'")
        if prod_id not in self.producer_subs:
            print(f"-- PRODUCER {prod_id} DOES NOT EXIST. SUB REQUEST FAIL.")

        # format for entry: "topic_id,highest_published_frame,highest_published_text"
        topic_published_counts = []

        for topic_id, counts in self.topic_info.items():
            if topic_id.startswith(prod_id):
                topic_published_counts.append(
                    f"{topic_id},{counts[Labels.FRAME_COUNT]},{counts[Labels.TEXT_COUNT]}"
                )
                self.topic_info[topic_id][Labels.SUBS].add(cons_id)

        header = {
            HeaderData.PACKET_TYPE: PacketType.SUB_PRODUCER_ACK,
            HeaderData.PRODUCER_ID: prod_id,
        }
        # ';' separated topic_published_counts: 
        msg = bytearray(f"ACK;{';'.join(topic_published_counts)}".encode())
        self._send(
            header_data=header, payload=msg, 
            target_ip=cons_id, target_port=CONSUMER_PORT
        )
        
        print("Sub request completed - ", topic_id)

    def unsub_from_prod(self, cons_ip: str, prod_id: str) -> None:
        if prod_id not in self.producer_subs:
            print(f"-- Producer {prod_id} doesn't exist; can't unsubscribe--")
            return

        # remove from topic's subscriber set
        for topic_id in self.topic_info.keys():
            if topic_id.startswith(prod_id):
                self.topic_info[topic_id][Labels.SUBS].remove(cons_ip)

        # remove from prod subs
        self.producer_subs[prod_id].remove(cons_ip)

        # send ACK
        header = {
            HeaderData.PACKET_TYPE: PacketType.UNSUB_PRODUCER_ACK,
            HeaderData.PRODUCER_ID: prod_id,
        }
        msg = bytearray(f"ACK: Broker unsubbed from producer {prod_id}".encode())
        self._send(
            header_data=header, payload=msg, 
            target_ip=cons_ip, target_port=CONSUMER_PORT
        )
        
        print("-- Unsub request completed - ", prod_id, " --")