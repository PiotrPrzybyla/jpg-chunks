from chunki import read_chunk, additional_chunks, main_chunks
from transformata import transform

name = 'MgławicaOriona.png'


with open(name, 'rb') as f:
    header = f.read(8)

    if header != b'\x89PNG\r\n\x1a\n':
        print("To nie jest plik PNG")
    else:
        print("To jest plik PNG")

        while True:
            chunk_length, chunk_type, chunk_data, chunk_crc = read_chunk(f)
            if chunk_type == 'IHDR':
                main_chunks(chunk_data)
                print("")
                transform(name)
                additional_chunks(name)

            elif chunk_type == 'IEND':
                break
