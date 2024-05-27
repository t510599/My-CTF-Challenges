import zlib
import binascii

from enum import Enum

PNG_MAGIC = b'\x89PNG\r\n\x1a\n'
PNG_IHDR = b'IHDR'
PNG_IDAT = b'IDAT'
PNG_IEND = b'IEND'

class PNGIHDREnum(Enum):
    def to_bytes(self):
        return self.value.to_bytes(1, 'big')


class PNGColorType(PNGIHDREnum):
    GRAYSCALE = 0
    TRUECOLOR = 2
    INDEXED_COLOR = 3
    GRAYSCALE_ALPHA = 4
    TRUECOLOR_ALPHA = 6


class PNGFilter(PNGIHDREnum):
    NONE = 0
    SUB = 1
    UP = 2
    AVERAGE = 3
    PAETH = 4


class PNGInterlace(PNGIHDREnum):
    NONE = 0
    ADAM7 = 1


class PNGCompression(PNGIHDREnum):
    DEFLATE = 0


def create_chunk(chunk_type, data=b''):
    return len(data).to_bytes(4, 'big') + chunk_type + data + binascii.crc32(chunk_type + data).to_bytes(4, 'big')


def create_header(
        width, height,
        bit_depth=8,
        color_type=PNGColorType.GRAYSCALE,
        compression=PNGCompression.DEFLATE,
        filter_method=PNGFilter.NONE,
        interlace_method=PNGInterlace.NONE
):
    data = width.to_bytes(4, 'big') + height.to_bytes(4, 'big') + \
        bit_depth.to_bytes() + color_type.to_bytes() + \
        compression.to_bytes() + filter_method.to_bytes() + interlace_method.to_bytes()
    
    return create_chunk(PNG_IHDR, data)


def create_idat_filter_none(width, height, data):
    scanline_size = width + 1
    scanline = b'\x00' + data[:scanline_size]
    filtered_data = bytearray(scanline)
    
    for i in range(scanline_size, len(data), scanline_size):
        scanline = data[i:i + scanline_size]
        filtered_data.append(0)
        filtered_data.extend(scanline)
    
    return bytes(filtered_data)


def create_png(width, height, data):
    idat = create_idat_filter_none(width, height, data)
    idat = zlib.compress(idat, level=0)

    return PNG_MAGIC + \
        create_header(width, height) + \
        create_chunk(PNG_IDAT, idat) + \
        create_chunk(PNG_IEND)


with open("solve0.png", "wb") as f:
    im = create_png(1, 1, b'\x00')
    f.write(im)


with open("solve255.png", "wb") as f:
    im = create_png(1, 1, b'\xff')
    f.write(im)