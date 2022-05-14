import os
from PIL import Image
import json
# opening png
png = Image.open("input_pictos/pictos-sprite.png")
css = 'input_pictos/pictos-sprite.css' # css file
# how many pictos
manypictos = png.size[0] / 256
# width and height
width, height = png.size
# default values
left = 0
top = height - 256
right = 256
bottom = 2 * height - 256
# opening css
i = 0
for line in open(css):
    while ((line[(i - 1):i]) == "{") == False:
        i += 1
    if ((line[(i - 1):i]) == "{") == True:
        i -= 1
        picto = (line[7:i])
        i = 0
        cropped_picto = png.crop((left, top, right, bottom))
        cropped_picto.save("output_png/" + picto + ".png")
        left += 256
        right += 256
