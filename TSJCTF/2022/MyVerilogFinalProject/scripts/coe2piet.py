from PIL import Image
import sys
import re

# LIGHT RED     #FFC0C0 7 6 3 | 1
# LIGHT YELLOW  #FFFFC0 7 7 3 | 2
# LIGHT GREEN   #C0FFC0 6 7 3 | 3
# LIGHT CYAN    #C0FFFF 6 7 3 | 3
# LIGHT BLUE    #C0C0FF 6 6 3
# LIGHT MAGENTA #FFC0FF 7 6 3 | 1
#       RED     #FF0000 7 0 0
#       YELLOW  #FFFF00 7 7 0
#       GREEN   #00FF00 0 7 0
#       CYAN    #00FFFF 0 7 3
#       BLUE    #0000FF 0 0 3 | 4
#       MAGENTA #FF00FF 7 0 3
# DARK  RED     #C00000 6 0 0
# DARK  YELLOW  #C0C000 6 6 0
# DARK  GREEN   #00C000 0 6 0
# DARK  CYAN    #00C0C0 0 6 3
# DARK  BLUE    #0000C0 0 0 3 | 4
# DARK  MAGENTA #C000C0 6 0 3
# WHITE         #FFFFFF 7 7 3 | 2
# BLACK         #000000 0 0 0

table = {
    (7, 6, 3): 0xFFC0C0,
    # (7, 7, 3): 0xFFFFC0,
    (6, 7, 3): 0xC0FFC0,
    # (6, 7, 3): 0xC0FFFF,
    (6, 6, 3): 0xC0C0FF,
    # (7, 6, 3): 0xFFC0FF,
    (7, 0, 0): 0xFF0000,
    (7, 7, 0): 0xFFFF00,
    (0, 7, 0): 0x00FF00,
    (0, 7, 3): 0x00FFFF,
    (0, 0, 3): 0x0000FF,
    (7, 0, 3): 0xFF00FF,
    (6, 0, 0): 0xC00000,
    (6, 6, 0): 0xC0C000,
    (0, 6, 0): 0x00C000,
    (0, 6, 3): 0x00C0C0,
    # (0, 0, 3): 0x0000C0,
    (6, 0, 3): 0xC000C0,
    (7, 7, 3): 0xFFFFFF,
    (0, 0, 0): 0x000000
}

def parse_vector(s):
    h = int(s, 16)
    r = (h & 0b11100000) >> 5
    g = (h & 0b11100) >> 2
    b = h & 0b11

    v = table[(r,g,b)]
    return v >> 16, (v & 0xFF << 8) >> 8, v & 0xFF

h, w = None, None
pixels = []

with open(sys.argv[1], "r", encoding="utf-8") as f:
    lines = f.readlines()
    h, w = map(int, re.findall(r"Height: (\d+), Width: (\d+)", lines[2])[0])
    pixels = [parse_vector(s) for s in "".join(map(str.strip, lines[5:]))[:-1].split(",")]

img = Image.new("RGB", (w, h))

for i, p in enumerate(pixels):
    img.putpixel((i % img.width, i // img.width), p)

img.save("output.png")