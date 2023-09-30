import socket
import struct
from util import PacketType, HeaderData, Labels, BUFFER_SIZE
from typing import Dict, Any, Tuple

class ProtocolSocketBase:
    def __init__(self, ip: str, port: str) -> None:
        self._local_ip = ip
        self._local_port = port
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((self._local_ip, self._local_port))

    def _create_header(
            self, packet_type: PacketType, prod_id: str, stream_id: int, frame_id: int
    ) -> bytearray:
        stream_id = int(stream_id) # ensure its int

        header = bytearray()
        header.extend(struct.pack('B', packet_type.value)) # 'B' = 1 byte
        prod_id_byte = bytes.fromhex(prod_id)
        assert(len(prod_id_byte) == 3) # must be 3 bytes
        header.extend(bytearray(prod_id_byte))
        header.extend(struct.pack('B', stream_id)) # single producer can have at most 8 simultaneous streams
        header.extend(struct.pack('i', frame_id)) # 'i' = signed integer (4 bytes)

        return header

         
    def _send(
        self, header_data: Dict[HeaderData, Any],
        payload: bytearray, target_ip: str, target_port: str
    ) -> bool:
        header = self._create_header(
            header_data.get(HeaderData.PACKET_TYPE),
            header_data.get(HeaderData.PRODUCER_ID, b'AAA'),
            header_data.get(HeaderData.STREAM, 0),
            header_data.get(HeaderData.FRAME, 0)
        )
        data = header + payload

        if len(data) > BUFFER_SIZE:
            print("!!!\n len(data) > BUFFER_SIZE \n!!!")

        self.UDPSocket.sendto(data, (target_ip, target_port))

    def _receive(self, buffer_size: int = BUFFER_SIZE) -> Tuple[Dict[str, Any], Tuple[str, int]]:
        msg, addr = self.UDPSocket.recvfrom(buffer_size)
        return (self._parse_packet(msg), addr)

    def _parse_packet(self, payload: bytes) -> Dict[str, Any]:
        return {
            Labels.PACKET_TYPE: payload[0],
            Labels.PRODUCER_ID: bytes(payload[1:4]), # bytes, need to do .hex() to get str
            Labels.STREAM_ID: payload[4],
            Labels.FRAME_ID: payload[5],
            Labels.BODY: bytes(payload[6:])
        }
