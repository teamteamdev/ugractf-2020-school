#!/usr/bin/env python3

import hmac
import io
import json
import os
import PIL.Image, PIL.ImageDraw, PIL.ImageFont
import random
import statistics
import sys

PREFIX = "ugra_who_s_that_writin_john_the_revelator_"
SECRET = b"worthy-where-choose-flock-bush"
SALT_SIZE = 12

def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    user_id = sys.argv[1]
    target_dir = sys.argv[2]

    flag = get_flag()

    random.seed(hmac.new(SECRET, str(user_id).encode(), "sha256").digest())

    font = PIL.ImageFont.load(os.path.join("private", "ter-u14b_iso-8859-1.pil"))

    text_image = PIL.Image.new("RGB", (len(flag) * 8 + 3, 16))
    draw = PIL.ImageDraw.ImageDraw(text_image)
    draw.text((2, 0), flag, font=font, fill=(255, 255, 255))
    text_image = text_image.resize((text_image.size[0] * 4, text_image.size[1] * 4))

    while True:
        palette = list(range(256)) * 3
        random.shuffle(palette)

        colors = list(range(256))
        random.shuffle(colors)
        colors = (colors[:32], colors[32:])

        channels = [[palette[i * 3 + ch] for i in range(256)] for ch in range(3)]
        means0 = [statistics.mean([channels[ch][c] for c in colors[0]]) for ch in range(3)]
        means1 = [statistics.mean([channels[ch][c] for c in colors[1]]) for ch in range(3)]

        if max(abs(a - b) for a, b in zip(means0, means1)) < 5:
            break

    image = PIL.Image.new("P", text_image.size)
    image.putpalette(palette)

    pixels = image.load()
    text_pixels = text_image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixels[x, y] = random.choice(colors[text_pixels[x, y] != (0, 0, 0)])

    image.save(os.path.join(target_dir, "camo.png"))

    json.dump({"flags": [flag], "substitutions": {}, "urls": []}, sys.stdout)


if __name__ == "__main__":
    generate()
