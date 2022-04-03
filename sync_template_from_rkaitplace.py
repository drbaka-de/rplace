from PIL import Image, ImageOps
import requests
from io import BytesIO
import re
import binascii
import numpy as np
import math

def update_from_upstream(original_url, filename):
	# download template from upstream
	original_url = 
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
		img = Image.open(filename)

	# fix colors
	palette = [0x6d001a, 0xBE0039, 0xFF4500, 0xFFA800, 0xFFD635, 0xfff8b8, 0x00A368, 0x00CC78, 0x7EED56, 0x00756F, 0x009EAA, 0x00ccc0, 0x2450A4, 0x3690EA, 0x51E9F4, 0x493AC1, 0x6A5CFF, 0x94b3ff, 0x811E9F, 0xB44AC0, 0xe4abff, 0xde107f, 0xFF3881, 0xFF99AA, 0x6D482F, 0x9C6926, 0xffb470, 0x000000, 0x515252, 0x898D90, 0xD4D7D9, 0xFFFFFF]

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
		img.save(filename)
		return img

# create overlay

kit_image = update_from_upstream("https://rkaitplace.netlify.app/", "reference.png")
kit_image = kit_image.resize((kit_image.size[0] * 3, kit_image.size[1] * 3), Image.NEAREST)

koeri_image = update_from_upstream("https://rkaitplace.netlify.app/koeri.html", "reference_koeri.png")
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