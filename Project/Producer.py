import os
from typing import Dict, List
import sys

from ProtocolSocketBase import ProtocolSocketBase
from util import *


class Producer(ProtocolSocketBase):
    def __init__(self, local_ip: str = "producer0") -> None:
        # enable passing of ip in command line
        if len(sys.argv) > 1:
            local_ip = sys.argv[1]
        super().__init__(local_ip, PRODUCER_PORT)
        self.prod_id = os.urandom(3).hex() # random 3 byte string
        self.streams: Dict[int, List[int]] = {} # stream_id: [cur_frame_count, cur_text_count]
    
    def publish_new_stream(self, stream_id: str) -> None:
        topic_id = f"{self.prod_id}{stream_id}"
        print(f"Publishing stream {stream_id}. (Topic {topic_id})")
        self.streams[int(stream_id)] = [0, 0] # start at frame 0, text 0
        
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

    def publish_content(self, stream_id: str, file_path: str) -> None:
        stream_id = int(stream_id)
        ext = os.path.splitext(file_path)[1]
        is_frame = True if ext != ".txt" else False

        if stream_id not in self.streams:
            print(f"-- Stream {stream_id} has not been announced; will not send content --")
            return
        
        header = {
            HeaderData.PRODUCER_ID: self.prod_id,
            HeaderData.STREAM: stream_id
        }
        data = bytearray()
        if is_frame:
            header[HeaderData.PACKET_TYPE] = PacketType.SEND_FRAME
            header[HeaderData.FRAME] = self.streams[stream_id][0]
            self.streams[stream_id][0] += 1
            data = file_to_bytes(file_path)
        else:
            header[HeaderData.PACKET_TYPE] = PacketType.SEND_TEXT
            header[HeaderData.TEXT] = self.streams[stream_id][1]
            self.streams[stream_id][1] += 1
            data = text_file_to_bytes(file_path)

        self._send(header, BROKER_IP, BROKER_PORT, data)

        print("-- data sent to broker --")
        print(data)
        print("--")
