import PIL.Image
import json

def cutAtlas(pngFile, jsonFile, output):
	with open(jsonFile) as f:
		atlas = json.load(f)
	sprite = PIL.Image.open(pngFile)
	pictoWidth = atlas["imageSize"]["width"]
	pictoHeight = atlas["imageSize"]["height"]
	if sprite.width != pictoWidth * 7:
		sprite = sprite.resize(pictoWidth * 7, round(sprite.height * (pictoWidth * 7 / sprite.width)))
	for picto in atlas["images"]:
		print(picto)
		x1 = atlas["images"][picto]["width"]
		y1 = atlas["images"][picto]["height"]
		x2 = x1 + pictoWidth
		y2 = y1 + pictoHeight
		sprite.crop((x1, y1, x2, y2)).save(f"{output}/{picto}.png")
	