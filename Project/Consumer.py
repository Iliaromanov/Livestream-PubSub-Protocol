from typing import Dict, List
import threading
import sys

from ProtocolSocketBase import ProtocolSocketBase
from util import *


class Consumer(ProtocolSocketBase):
    def __init__(self, local_ip: str = "consumer0") -> None:
        # enable passing of ip in command line
        if len(sys.argv) > 1:
            local_ip = sys.argv[1]
        super().__init__(local_ip, CONSUMER_PORT)
        self.cons_id = local_ip
        self.subscription_frame_counts: Dict[str, List[int]] = {} # topic_id: [frame_count, text_count]

        self.start_listening_for_content()
  
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

        # needed so that the content listener doesn't receive ACK
        self.stop_listening_for_content()
        
        # receive ACK and highest frame published from Broker
        data = self._receive()[0]
        assert(data[Labels.PACKET_TYPE] == PacketType.SUB_STREAM_ACK.value)
        assert(data[Labels.STREAM_ID] == int(stream_id))

        # set max frame and text counts
        self.subscription_frame_counts[topic_id][0] = data[Labels.FRAME_ID]
        self.subscription_frame_counts[topic_id][1] = data[Labels.TEXT_ID]

        print("-- Reply from Broker - ", data[Labels.BODY])

        self.start_listening_for_content()

    def start_listening_for_content(self) -> None:
        # runs the self.listen_and_process_content in thread
        self.content_listen = True
        self.content_listen_thread = threading.Thread(target=self.listen_and_process_content)
        self.content_listen_thread.start()

    def stop_listening_for_content(self) -> None:
        self.content_listen = False
        self.content_listen_thread.join()

    def listen_and_process_content(self) -> None:
        # calls recvfrom and parses output into self.subscription_frame_counts
        while self.content_listen:
            data = self._receive()[0]

            packet_type = data[Labels.PACKET_TYPE]
            prod_id = data[Labels.PRODUCER_ID]
            stream_id = data[Labels.STREAM_ID]
            frame_id = data[Labels.FRAME_ID]
            text_id = data[Labels.TEXT_ID]
            content = data[Labels.BODY]

            topic_id = f"{prod_id}{stream_id}"

            print(f"-- Recevied content for topic {topic_id} --")

            is_frame = True if packet_type == PacketType.SEND_FRAME.value else False
            assert(
                (is_frame and packet_type == PacketType.SEND_FRAME.value) or 
                (not is_frame and packet_type == PacketType.SEND_TEXT.value)    
            )

            # check cur highest counts
            counts = self.subscription_frame_counts[topic_id]
            cur_highest = counts[0] if is_frame else counts[1]
            sent_count = max(frame_id, text_id) # cus default is 0 so higher one is the one sent

            if sent_count <= cur_highest:
                print(f"-- Seen a frame/text >= {sent_count}; not receiving --")
                return
            
            # update cur highest counts
            if is_frame:
                counts[0] = sent_count
            else:
                counts[1] = sent_count

            print("-- Content text/frame received and processed: ")
            print(content)
            print("--")

            print(f"Consumer - {self.cons_id} - waiting on input ...\n> ")

    def unsubscribe_stream(self, prod_id: str, stream_id: str) -> None:
        topic_id = f"{prod_id}{stream_id}"
        if topic_id not in self.subscription_frame_counts:
            print(f"-- Not currently subscribed to topic {topic_id}; can't unsub")
            return
        
        header = {
            HeaderData.PACKET_TYPE: PacketType.UNSUB_STREAM,
            HeaderData.PRODUCER_ID: prod_id,
            HeaderData.STREAM: stream_id
        }

        self._send(header, BROKER_IP, BROKER_PORT)

        # Wait for ACK
        # needed so that the content listener doesn't receive ACK
        self.stop_listening_for_content()

        data = self._receive()[0]
        assert(data[Labels.PACKET_TYPE] == PacketType.UNSUB_STREAM_ACK.value)
        assert(data[Labels.STREAM_ID] == int(stream_id))

        print("-- Reply from Broker - ", data[Labels.BODY])

        self.start_listening_for_content()


    def subscribe_producer(self, prod_id: str) -> None:
        pass

    def unsubscribe_producer(self, prod_id: str) -> None:
        pass


        