import socket
import struct
from util import PacketType, HeaderData, BUFFER_SIZE
from typing import Dict, Any, Tuple

class ProtocolSocketBase:
    def __init__(self, ip: str, port: str) -> None:
        self._local_ip = ip
        self._local_port = port
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((self._local_ip, self._local_port))

    def _create_header(
            self, packet_type: PacketType, prod_id: bytes, stream: int, frame: int
    ) -> bytearray:
        header = bytearray()
        header.extend(struct.pack('B', packet_type.value)) # 'B' = 1 byte
        assert(len(prod_id) == 3) # must be 3 bytes
        header.extend(bytearray(prod_id))
        header.extend(struct.pack('B', stream))
        header.extend(struct.pack('i', frame)) # 'i' = signed integer (4 bytes)

        return header

         
    def _send(
        self, header_data: Dict[HeaderData, Any],
        payload: bytearray, target_ip: str, target_port: str
    ) -> bool:
        header = self._create_header(
            header_data.get(HeaderData.PACKET_TYPE),
            header_data.get(HeaderData.PRODUCER_ID),
            header_data.get(HeaderData.STREAM, 0),
            header_data.get(HeaderData.FRAME, 0)
        )
        data = header + payload

        self.UDPSocket.sendto(data, (target_ip, target_port))

    def _receive(self, buffer_size: int = BUFFER_SIZE) -> Tuple[bytes, str]:
        msg, addr = self.UDPSocket.recvfrom(buffer_size)
        return (msg, addr)

    def _parse_packet(self, payload: bytes) -> Dict[str, Any]:
        return {
            "packet_type": payload[0],
            "producer_id": bytes(payload[1:4]), # bytes, need to do .hex() to get str
            "stream": payload[4],
            "frame": payload[5],
            "payload": bytes(payload[6:])
        }
