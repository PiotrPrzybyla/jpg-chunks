import struct

from PIL import Image

from PIL.ExifTags import TAGS

from anonimizacja import anonymize_png
from read_write import read_chunk

counter = 1
chunki = {0: "Domyślne"}



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


def read_png_chunks(file_path):
    global counter
    global chunki
    with open(file_path, 'rb') as f:
        f.read(8)
        while True:
            chunk_length, chunk_type, chunk_data, chunk_crc = read_chunk(f)
            if chunk_type is None:
                break
            if chunk_type == 'iCCP':
                chunki[counter] = 'iCCP'
                counter = counter+1
                profile_name, compression_method, compressed_profile = chunk_data.split(b'\x00', 2)
                compression_method = int.from_bytes(compression_method, 'big')
                print(f"Profile name: {profile_name.decode()}")
                print(f"Compression method: {compression_method}")
                print(f"Decompressed profile size: {get_icc_profile(file_path)}")
            elif chunk_type == 'bKGD':
                chunki[counter] = 'bKGD'
                counter = counter + 1
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
            elif chunk_type == 'pHYs':
                chunki[counter] = 'pHYs'
                counter = counter + 1
                pixels_per_unit_x = int.from_bytes(chunk_data[:4], 'big')
                pixels_per_unit_y = int.from_bytes(chunk_data[4:8], 'big')
                print(f"pHYs chunk: pixels per unit - x: {pixels_per_unit_x}, y: {pixels_per_unit_y}")
            elif chunk_type == 'hIST':
                chunki[counter] = 'hIST'
                counter = counter + 1
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
            elif chunk_type == 'tIME':
                chunki[counter] = 'tIME'
                counter = counter + 1
                year = int.from_bytes(chunk_data[:2], 'big')
                month = chunk_data[2]
                day = chunk_data[3]
                hour = chunk_data[4]
                minute = chunk_data[5]
                second = chunk_data[6]
                print(f"tIME chunk: {year}-{month:02}-{day:02} {hour:02}:{minute:02}:{second:02}")


def get_png_info(image_path):
    image = Image.open(image_path)
    png_info = image.info
    print(png_info)
    return png_info


def convert_byte_to_int_or_string(data):
    if isinstance(data, bytes):
        if data.startswith(b'ASCII'):
            string_data = data.decode('utf-8')
            string_data = string_data.replace("ASCII", "")
            return string_data
        integer_value = int.from_bytes(data, byteorder='big')
        return integer_value
    else:
        return data


def get_exif(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            value = convert_byte_to_int_or_string(value)
            print(f"{tag_name}: {value}")


def get_icc_profile(image_path):
    image = Image.open(image_path)
    icc_profile = image.info.get('icc_profile')
    if icc_profile:
        return len(icc_profile)
    return None


def main_chunks(chunk_data):
    parse_ihdr(chunk_data)


def additional_chunks(name):
    read_png_chunks(name)
    get_icc_profile(name)
    get_exif(name)
    print("Które chunki animizować")
    for klucz, wartosc in chunki.items():
        print(f"{klucz}: {wartosc}")
    dane = input("Wprowadź dane, oddzielając je przecinkami: ")
    lista = dane.split(",")
    lista = [int(element) for element in lista]
    wartosci = list(map(chunki.get, lista))
    if 0 in lista:
        wartosci = []
    print(wartosci)
    anonymize_png(wartosci, name, 'output_image.png')