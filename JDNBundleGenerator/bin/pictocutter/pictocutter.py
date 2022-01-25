import os
from PIL import Image
import json
import sys
import urllib.request

codename = sys.argv[1]

urlpng = "http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/songs/" + codename + "/assets/web/pictos-sprite.png"
urlcss = "http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/songs/" + codename + "/assets/web/pictos-sprite.css"
urllib.request.urlretrieve(urlpng, "bin/pictocutter/picto_input/pictos-sprite.png")
urllib.request.urlretrieve(urlcss, "bin/pictocutter/picto_input/pictos-sprite.css")

# opening png
png = Image.open("bin/pictocutter/picto_input/pictos-sprite.png")
css = 'bin/pictocutter/picto_input/pictos-sprite.css' # css file
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
        cropped_picto.save("bin/pictos/" + codename + "/pictos/" + picto + ".png")
        left += 256
        right += 256
