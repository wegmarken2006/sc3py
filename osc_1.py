import struct

BYTEORDER = "big"


def encode_i8(val: int) -> bytes:
    return val.to_bytes(1, BYTEORDER)


def encode_i16(val: int) -> bytes:
    return val.to_bytes(2, BYTEORDER)


def encode_i32(val: int) -> bytes:
    return val.to_bytes(4, BYTEORDER)


def encode_i64(val: int) -> bytes:
    return val.to_bytes(8, BYTEORDER)


def decode_i8(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER)


def decode_i16(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER)


def decode_i32(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER)


def decode_i64(btes: bytes) -> int:
    return int.from_bytes(btes, BYTEORDER)


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


def str_pstr(st: str) -> bytes:
    return encode_i8(len(st)) + st.encode()
