import bz2
import gzip
import lzma
import struct
import zlib

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import piexif




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


def anonymize_png(input_path, output_path):
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        # Skopiuj nagłówek PNG
        f_out.write(f_in.read(8))

        while True:
            chunk_length, chunk_type, chunk_data, chunk_crc = read_chunk(f_in)

            # Zapisz tylko niezbędne chunki
            if chunk_type in {'IHDR', 'IDAT', 'IEND'}:
                write_chunk(f_out, chunk_length, chunk_type, chunk_data, chunk_crc)

            # Przerwij po chunku IEND
            if chunk_type == 'IEND':
                break


def read_chunkk(f):
    # Każdy chunk składa się z długości (4 bajty), typu (4 bajty), danych (długość bajtów) i CRC (4 bajty)
    length = struct.unpack('!I', f.read(4))[0]  # !I oznacza big-endian unsigned int
    chunk_type = f.read(4).decode('ascii')
    data = f.read(length)
    crc = struct.unpack('!I', f.read(4))[0]
    return chunk_type, data


def parse_ihdr(chunk_data):
    # IHDR chunk składa się z: szerokości (4 bajty), wysokości (4 bajty), głębii bitowej (1 bajt),
    # typu koloru (1 bajt), metody kompresji (1 bajt), metody filtra (1 bajt), interlace (1 bajt)
    width, height, bit_depth, color_type, compression_method, filter_method, interlace_method = struct.unpack('!II5B', chunk_data)
    global color_type_global
    color_type_global = color_type
    print(f"Width: {width} pixels")
    print(f"Height: {height} pixels")
    print(f"Bit depth: {bit_depth}")
    print(f"Color type: {color_type}")
    print(f"Compression method: {compression_method}")
    print(f"Filter method: {filter_method}")
    print(f"Interlace method: {interlace_method}")


def display_image(image_path):
    with Image.open(image_path) as img:
        img.show()


def display_spectrum(image_path):
    # Wczytaj obraz i przekształć go na skale szarości
    img = Image.open(image_path).convert('L')

    # Przekształć obraz na tablicę numpy
    img_data = np.asarray(img)

    # Przeprowadź transformację Fouriera
    fft_result = np.fft.fft2(img_data)

    # Przesuń zerową częstotliwość do środka
    fft_shifted = np.fft.fftshift(fft_result)

    # Oblicz widmo mocy
    spectrum = np.abs(fft_shifted)

    # Wyświetl widmo
    plt.imshow(np.log1p(spectrum), cmap='gray')
    plt.title('Spectrum')
    plt.show()


def test_fft(image_path):
    img = Image.open(image_path).convert('L')
    img_data = np.asarray(img)

    # Przeprowadź transformację Fouriera
    fft_result = np.fft.fft2(img_data)

    # Przeprowadź odwrotną transformację Fouriera
    ifft_result = np.fft.ifft2(fft_result)

    # Oblicz różnicę między oryginalnym obrazem a obrazem po transformacji i odwrotnej transformacji
    difference = np.abs(img_data - ifft_result)

    print(f"Maximum difference: {np.max(difference)}")



def read_png_chunks(file_path):
    with open(file_path, 'rb') as f:
        # Przeskocz nagłówek pliku
        f.read(8)
        while True:
            chunk_length, chunk_type, chunk_data, chunk_crc = read_chunk(f)
            if chunk_type is None:
                break

            # Chunk iCCP
            if chunk_type == 'iCCP':
                # # Podziel chunk_data na nazwę profilu i skompresowane dane profilu
                # profile_name, compressed_profile = chunk_data.split(b'\x00', 1)
                # decompressor = zlib.decompressobj()
                # print(compressed_profile)
                # try:
                #     decompressed_data = zlib.decompress(compressed_profile)
                # except zlib.error as e:
                #     print(f"Error decompressing iCCP chunk: {e}")
                # else:
                #     print(f"iCCP chunk: Profile name={profile_name}, Profile data={decompressed_data}")
                # profile_name, null_separator, compression_method, compressed_size, decompressed_size = chunk_data.split(b'\x00', 4)
                profile_name, compression_method, compressed_profile = chunk_data.split(b'\x00', 2)
                print(chunk_data)
                decompressed_data = zlib.decompress(compressed_profile)
                # print(chunk_data)
                compression_method = int.from_bytes(compression_method, 'big')
                # compressed_size = int.from_bytes(compressed_size, 'big')
                # decompressed_size = int.from_bytes(decompressed_size, 'big')
                # compressed_size = int.from_bytes(compressed_size, 'big')
                # decompressed_size = int.from_bytes(decompressed_size, 'big')

                print(f"Profile name: {profile_name.decode()}")
                print(f"Compression method: {compression_method}")
                print(f"Compressed profile size: {compressed_profile}")
                # print(f"Decompressed profile size: {decompressed_size}")


            # Chunk bKGD
            elif chunk_type == 'bKGD':
                if color_type_global == 2 or color_type_global == 6:
                    red = int.from_bytes(chunk_data[:2], 'big')
                    green = int.from_bytes(chunk_data[2:4], 'big')
                    blue = int.from_bytes(chunk_data[4:], 'big')
                    print(f"bKGD chunk (RGB): red={red}, green={green}, blue={blue}")
                elif color_type_global == 3:
                    palette_index = chunk_data[0]
                    print(f"bKGD chunk (Indexed): palette index={palette_index}")
                elif color_type_global == 0 or  color_type_global == 4:
                    grey = int.from_bytes(chunk_data[:2], 'big')
                    print(f"bKGD chunk (Grey): grey={grey}")
                else:
                    print(f"bKGD chunk: {chunk_data}")

            # Chunk pHYs
            elif chunk_type == 'pHYs':
                # dane są zapisane jako dwie liczby całkowite 4-bajtowe
                pixels_per_unit_x = int.from_bytes(chunk_data[:4], 'big')
                pixels_per_unit_y = int.from_bytes(chunk_data[4:8], 'big')
                print(f"pHYs chunk: pixels per unit - x: {pixels_per_unit_x}, y: {pixels_per_unit_y}")
            # Chunk hIST
            elif chunk_type == 'hIST':
                if len(chunk_data) % 2 != 0:
                    print("Invalid hIST chunk data length.")
                    return

                num_entries = len(chunk_data) // 2
                histogram = []

                for i in range(num_entries):
                    entry = int.from_bytes(chunk_data[i * 2:i * 2 + 2], 'big')
                    histogram.append(entry)

                print("Histogram:")
                for i, count in enumerate(histogram):
                    print(f"Color index {i}: {count} occurrences")
            # Chunk tIME
            elif chunk_type == 'tIME':
                # dane są zapisane jako liczby całkowite 2-bajtowe i 1-bajtowe
                year = int.from_bytes(chunk_data[:2], 'big')
                month = chunk_data[2]
                day = chunk_data[3]
                hour = chunk_data[4]
                minute = chunk_data[5]
                second = chunk_data[6]
                print(f"tIME chunk: {year}-{month:02}-{day:02} {hour:02}:{minute:02}:{second:02}")


with open('Floral-PNG-File.png', 'rb') as f:
    header = f.read(8)
    name = 'Floral-PNG-File.png'
    if header != b'\x89PNG\r\n\x1a\n':
        print("To nie jest plik PNG")
    else:
        print("To jest plik PNG")

        while True:
            chunk_type, chunk_data = read_chunkk(f)
            if chunk_type == 'IHDR':
                parse_ihdr(chunk_data)
                # display_image('image.png')
                # display_spectrum('image.png')
                test_fft(name)
                anonymize_png(name, 'output_image.png')
                read_png_chunks(name)
            elif chunk_type == 'IEND':
                break
