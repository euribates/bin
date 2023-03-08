#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont


# FONT_NAME = "FreeMono.ttf"
FONT_NAME = "FiraMono-Regular.otf"
FONT_SIZE = 20
BACKGROUND = (0, 0, 0)
COLOR = (255, 198, 128)
BORDER = 6
PADDING = BORDER // 2


def main():
    email = sys.argv[1]
    font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
    canvas = Image.new("RGB", (2, 2), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    width, height = draw.textsize(email, font=font)
    width += BORDER
    height += BORDER
    img = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(img)
    draw.text((PADDING, PADDING), email, font=font, fill=COLOR)
    img.show()


if __name__ == "__main__":
    main()
