import PIL.Image
import PIL.ImageTk
import os, sys
from tkinter import *
from tkinter import filedialog
import json
import pathlib
import time
time.sleep(0.8)

openFile = Tk()
openFile.title('File Open (ignore this window)')
ofcDir = str(pathlib.Path().absolute())

pngFile = openFile.filename = "input_pictos\pictos-atlas.png"
jsonFile = openFile.filename = "input_pictos\pictos-atlas.json"
with open(jsonFile) as raw:
	jsonData = json.load(raw)
fp = open(pngFile,"rb")
pngLoad = PIL.Image.open(fp)

totalPictos = len(jsonData['images'])
pictosList = list(jsonData['images'])
widthSize = jsonData['imageSize']['width']
heigthSize = jsonData['imageSize']['height']

running = True
cP = 0
while running:
	if cP < totalPictos:
		print(pictosList[cP] + ': ')
		cXY = jsonData['images'][pictosList[cP]]
		print(cXY)
		left = cXY[0]
		top = cXY[1]
		right = cXY[0] + widthSize
		bottom = cXY[1] + heigthSize
		cropped_example = pngLoad.crop((left, top, right, bottom))
		cropped_example.save("output_png/" + pictosList[cP] + ".png")
	else:
		running = False

	cP += 1
	pass