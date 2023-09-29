import socket
import struct
from util import PacketType, HeaderData
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
        header.append(struct.pack('B', packet_type)) # 'B' = 1 byte
        assert(len(prod_id) == 3) # must be 3 bytes
        header.extend(bytearray(prod_id))
        header.append(struct.pack('B', stream))
        header.append(struct.pack('B', frame))

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

    def _receive(self, buffer_size: int) -> Tuple[bytes, str]:
        msg, addr = self.UDPSocket.recvfrom(buffer_size)
        return (msg, addr)
