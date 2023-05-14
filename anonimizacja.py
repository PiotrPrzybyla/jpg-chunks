from read_write import read_chunk, write_chunk
from PIL import Image


def display_image(image_path):
    with Image.open(image_path) as img:
        img.show()


def anonymize_png(lista, input_path, output_path):

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        # Skopiuj nagłówek PNG
        f_out.write(f_in.read(8))

        while True:
            chunk_length, chunk_type, chunk_data, chunk_crc = read_chunk(f_in)
            main_chunks = {'IHDR', 'IDAT', 'IEND'}
            main_chunks = main_chunks | set(lista)
            # Zapisz tylko niezbędne chunki
            if chunk_type in main_chunks:
                write_chunk(f_out, chunk_length, chunk_type, chunk_data, chunk_crc)

            # Przerwij po chunku IEND
            if chunk_type == 'IEND':
                break
    display_image(input_path)
    display_image(output_path)
