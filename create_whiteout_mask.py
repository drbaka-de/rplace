from PIL import Image, ImageOps

def main():
    mask = Image.new('RGB', (6000, 6000))
    mask_pixel = Image.new('RGB', (3, 3))
    for i in range(3):
        mask_pixel.putpixel((0,i), (0xff,0xff,0xff))
        mask_pixel.putpixel((i,0), (0xff,0xff,0xff))

    empty = Image.new('RGB', (6000, 6000))

    for x in range(2000):
        for y in range(2000):
            empty.paste(mask_pixel, (x*3, y*3))

    empty.save("mask.png")

if __name__ == "__main__":
    main()
