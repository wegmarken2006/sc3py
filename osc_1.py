import struct
from typing import Union, List
import socket

BYTEORDER = "big"


Datum = Union[int, float, str, bytes]

class Message:
    def __init__(self, name: str, ldatum: List[Datum]):
        self.name = name
        self.ldatum = ldatum

def encode_i8(val: int) -> bytes:
    return val.to_bytes(1, BYTEORDER, signed=True)


def encode_i16(val: int) -> bytes:
    return val.to_bytes(2, BYTEORDER, signed=True)


def encode_i32(val: int) -> bytes:
    return val.to_bytes(4, BYTEORDER, signed=True)


def encode_i64(val: int) -> bytes:
    return val.to_bytes(8, BYTEORDER, signed=True)


def decode_i8(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER, signed=True)


def decode_i16(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER, signed=True)


def decode_i32(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER, signed=True)


def decode_i64(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER, signed=True)


def encode_f32(val: float) -> bytes:
    return struct.pack(">f", val)


def encode_f64(val: float) -> bytes:
    return struct.pack(">d", val)


def decode_f32(btes: bytes) -> float:
    return struct.unpack(">f", btes)[0]


def decode_f64(btes: bytes) -> float:
    return struct.unpack(">d", btes)[0]


def encode_str(st: str) -> bytes:
    return st.encode()

def encode_string(st: str) -> bytes:
    return extend_(b'\x00', st.encode())

def str_pstr(st: str) -> bytes:
    return encode_i8(len(st)) + st.encode()

def align(n: int):
    return 4 - n%4

def extend_(pad: bytes, bts: bytes) -> bytes:
    n = align(len(bts))
    return bts + pad*n


def encode_blob(bts: bytes) -> bytes:
    b1 = encode_i32(len(bts))
    return b1 + extend_(b'\x00', bts)


def encode_datum(dt: Datum) -> bytes:
    if isinstance(dt, int):
        return encode_i32(dt)
    elif isinstance(dt, float):
        return encode_f64(dt)
    elif isinstance(dt, str):
        return encode_string(dt)
    elif isinstance(dt, bytes):
        return encode_blob(dt)

def tag(dt: Datum) -> str:
    if isinstance(dt, int):
        return "i"
    elif isinstance(dt, float):
        return "f"
    elif isinstance(dt, str):
        return "s"
    elif isinstance(dt, bytes):
        return "b"

def descriptor(ld: List[Datum]) -> str:
    out: str = ","
    for dt in ld:
        out = out + tag(dt)
    return out

def encode_message(msg: Message) -> bytes:
    es = encode_datum(msg.name)
    ds1 = encode_datum(descriptor(msg.ldatum))
    ds2 = [elem for elem in map(encode_datum, msg.ldatum)]
    return es + ds1 + b''.join(ds2)


UDP_IP = "127.0.0.1"
UDP_PORT = 57110
ADD_TO_TAIL = 1

def osc_setport(port: int):
    global UDP_PORT
    UDP_PORT = port

def osc_send(msg: bytes):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (UDP_IP, UDP_PORT))
    sock.settimeout(2) #2 secs timeout
    try:
        rec = sock.recv(1024)
        print(rec)
    except:
        pass

def send_message(msg: Message):
    bmsg = encode_message(msg)
    #print(bmsg)
    osc_send(bmsg)

def sc_start():
    osc_setport(57110)
    msg1 = Message(name="/notify", ldatum=[1])
    send_message(msg1)
    msg1 = Message(name="/g_new", ldatum=[1, ADD_TO_TAIL, 0])
    send_message(msg1)

