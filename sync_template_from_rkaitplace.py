from distutils.file_util import write_file
from PIL import Image, ImageOps
import requests
from io import BytesIO
import re
import binascii
import numpy as np
from sync_template import main

palette = np.array([0x6d001a, 0xBE0039, 0xFF4500, 0xFFA800, 0xFFD635, 0xfff8b8, 0x00A368, 0x00CC78, 0x7EED56, 0x00756F, 0x009EAA, 0x00ccc0, 0x2450A4, 0x3690EA, 0x51E9F4, 0x493AC1, 0x6A5CFF, 0x94b3ff, 0x811E9F, 0xB44AC0, 0xe4abff, 0xde107f, 0xFF3881, 0xFF99AA, 0x6D482F, 0x9C6926, 0xffb470, 0x000000, 0x515252, 0x898D90, 0xD4D7D9, 0xFFFFFF])

def l2diff(a,b):
	s = ((a & 0xff) - (b & 0xff))**2
	s += (((a>>8) & 0xff) - ((b>>8) & 0xff))**2
	s += (((a>>16) & 0xff) - ((b>>16) & 0xff))**2
	return s


def fix_colors(img):
	img = img.convert("RGBA")
	print("fix colors")
	print(img)
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			p = img.getpixel((x, y))
			original_color = (p[0] << 16) + (p[1] << 8) + p[2]
			palette_diff = [l2diff(original_color, pc) for pc in palette]
			palette_i = np.argmin(palette_diff)
			c = palette[palette_i]
			print(hex(original_color), "->", hex(c), "at", x, y)
			img.putpixel((x, y), (c>>16 & 0xff, c>>8 & 0xff, c & 0xff, 0xff))
	return img


# download template from upstream
def fetch_reference(url):
	response = requests.get(url)
	b64pngregex = re.compile(r"^.*data:image/png;base64,([^\"]*).*$")
	for line in response.text.split("\n"):
		b64pngmatch = b64pngregex.match(line)
		if b64pngmatch:
			print("FOUND REFERENCE in " + url)
			return Image.open(BytesIO(binascii.a2b_base64(b64pngmatch.group(1))))

    
def rescale_heuristic(img):
	if img.size[0] > 80:
		return img.resize((img.size[0] // 10, img.size[1] // 10), Image.NEAREST)
  else
    return img


def update_reference(url, file):
	img = fetch_reference(url)

	if not img:
		img = Image.open(file)

	if img:
    img = rescale_heuristic(img)
		img = fix_colors(img)
		img.save(file)


if __name__ == "__main__":
	update_reference("https://rkaitplace.netlify.app/", "reference.png")
	update_reference("https://rkaitplace.netlify.app/koeri.html", "reference_koeri.png")

	# run other script
	main()
