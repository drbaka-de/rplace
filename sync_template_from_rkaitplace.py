from PIL import Image, ImageOps
import requests
from io import BytesIO
import re
import binascii
import numpy as np
import math

# download template from upstream

original_url = "https://rkaitplace.netlify.app/"
response = requests.get(original_url)
b64pngregex = re.compile(r"^.*\"data:image/png;base64,([^\"]*).*$")
img = None
for line in response.text.split("\n"):
	b64pngmatch = b64pngregex.match(line)
	if b64pngmatch:
		print("FOUND REFERENCE")
		img = Image.open(BytesIO(binascii.a2b_base64(b64pngmatch.group(1))))
		break

if not img:
	img = Image.open("reference.png")

# fix colors

palette = [0xBE0039, 0xFF4500, 0xFFA800, 0xFFD635, 0x00A368, 0x00CC78, 0x7EED56, 0x00756F, 0x009EAA, 0x2450A4, 0x3690EA, 0x51E9F4, 0x493AC1, 0x6A5CFF, 0x811E9F, 0xB44AC0, 0xFF3881, 0xFF99AA, 0x6D482F, 0x9C6926, 0x000000, 0x898D90, 0xD4D7D9, 0xFFFFFF]

def l2diff(a,b):
	s = ((a & 0xff) - (b & 0xff))**2
	s += (((a>>8) & 0xff) - ((b>>8) & 0xff))**2
	s += (((a>>16) & 0xff) - ((b>>16) & 0xff))**2
	return s

if img:
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			p = img.getpixel((x, y))
			original_color = (p[0] << 16) + (p[1] << 8) + p[2]
			if original_color not in palette:
				palette_diff = [l2diff(original_color, pc) for pc in palette]
				palette_i = np.argmin(palette_diff)
				c = palette[palette_i]
				print(hex(original_color), "->", hex(c), "at", x, y)
				img.putpixel((x, y), (c>>16 & 0xff, c>>8 & 0xff, c & 0xff, 0xff))
	img.save("reference.png")

# create overlay

img = img.resize((img.size[0] * 3, img.size[1] * 3), Image.NEAREST)
img2 = Image.open("reference_koeri.png")
img2 = img2.resize((img2.size[0] * 3, img2.size[1] * 3), Image.NEAREST)
img3 = Image.open("reference_tichy.png")
img3 = img3.resize((img3.size[0] * 3, img3.size[1] * 3), Image.NEAREST)

mask_url = "https://media.discordapp.net/attachments/267492253168173056/959625681141104700/mask.png"
response = requests.get(mask_url)
mask_i = Image.open(BytesIO(response.content))
mask = Image.new("1", (3000, 3000), 0)
mask.paste(mask_i)
mask2 = Image.new("1", (3000*2, 3000*2), 0)
mask2.paste(mask_i, (0, 0))
mask2.paste(mask_i, (3000, 0))
mask2.paste(mask_i, (0, 3000))
mask2.paste(mask_i, (3000, 3000))

tl = (760 * 3, 521  * 3) # top left corner
tl2 = (1334 * 3, 754  * 3) # top left corner of img2
tl3 = (!!!CHANGEME!!! * 3, !!!CHANGEME!!!  * 3) # top left corner of img3

final_img = Image.new('RGBA', (3000, 3000))
unmasked_img = Image.new('RGBA', (3000, 3000))
unmasked_img.paste(img, tl)
final_img = Image.composite(final_img, unmasked_img, mask)
final_img.save("kait_overlay.png")

final_img2 = Image.new('RGBA', (3000*2, 3000*2))
unmasked_img2 = Image.new('RGBA', (3000*2, 3000*2))
unmasked_img2.paste(img, tl)
#unmasked_img2.paste(img2, tl2)
unmasked_img2.paste(img3, tl3)
final_img2 = Image.composite(final_img2, unmasked_img2, mask2)
#final_img2.save("kait_koeri_overlay.png")
final_img2.save("kait_tichy_overlay.png")
