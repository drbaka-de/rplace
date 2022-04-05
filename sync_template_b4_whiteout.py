from PIL import Image, ImageOps
import requests
from io import BytesIO

def main():
    mask = Image.open("mask.png").convert("1")
    b4_the_whiteout = Image.open("cxjalbw3hlr81.png").convert("RGBA")
    b4_the_whiteout = b4_the_whiteout.resize((b4_the_whiteout.size[0] * 3, b4_the_whiteout.size[1] * 3), Image.NEAREST)

    empty = Image.new('RGBA', (6000, 6000))
    b4_the_whiteout.paste(empty, None, mask)
    b4_the_whiteout.save("overlay.png")

if __name__ == "__main__":
    main()
