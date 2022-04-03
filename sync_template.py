from PIL import Image, ImageOps
import requests
from io import BytesIO

img = Image.open("reference.png")
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
