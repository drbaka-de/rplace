from PIL import Image, ImageOps
import requests
from io import BytesIO

def main():
    mask = Image.open("mask.png").convert("1")
    b4_the_whiteout = Image.open("cxjalbw3hlr81.png").convert("RGBA")

    empty = Image.new('RGBA', (6000, 6000))
    b4_the_whiteout.paste(empty, None, mask)
    b4_the_whiteout.save("overlay.png")

if __name__ == "__main__":
    main()
