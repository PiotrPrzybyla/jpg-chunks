import struct

def read_chunk(f):
    # Odczytaj długość chunka (4 bajty, big endian)
    chunk_length_data = f.read(4)
    if len(chunk_length_data) < 4:
        return None, None, None, None
    chunk_length = struct.unpack('>I', chunk_length_data)[0]

    # Odczytaj typ chunka (4 bajty)
    chunk_type = f.read(4).decode('ascii')

    # Odczytaj dane chunka (chunk_length bajtów)
    chunk_data = f.read(chunk_length)

    # Odczytaj CRC (4 bajty, big endian)
    chunk_crc = f.read(4)

    return chunk_length, chunk_type, chunk_data, chunk_crc


def write_chunk(f, chunk_length, chunk_type, chunk_data, chunk_crc):
    # Zapisz długość chunka (4 bajty, big endian)
    f.write(struct.pack('>I', chunk_length))

    # Zapisz typ chunka (4 bajty)
    f.write(chunk_type.encode('ascii'))

    # Zapisz dane chunka (chunk_length bajtów)
    f.write(chunk_data)

    # Zapisz CRC (4 bajty, big endian)
    f.write(chunk_crc)
