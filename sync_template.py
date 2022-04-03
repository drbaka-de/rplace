from PIL import Image, ImageOps
import requests
from io import BytesIO

def main():
    kit_image = Image.open("reference.png")
    kit_image = kit_image.resize((kit_image.size[0] * 3, kit_image.size[1] * 3), Image.NEAREST)
    koeri_image = Image.open("reference_koeri.png")
    koeri_image = koeri_image.resize((koeri_image.size[0] * 3, koeri_image.size[1] * 3), Image.NEAREST)

    mask = Image.open("mask.png").convert("1")

    top_left_kit = (760 * 3, 521 * 3)
    top_left_koeri = (601 * 3, 1887 * 3)

    empty = Image.new('RGBA', (6000, 6000))
    overlay = Image.new('RGBA', (6000, 6000))
    overlay.paste(kit_image, top_left_kit)
    overlay.paste(koeri_image, top_left_koeri)
    overlay.paste(empty, None, mask)
    overlay.save("overlay.png")

if __name__ == "__main__":
    main()