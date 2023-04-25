import os, sys, io, subprocess
from PIL import Image

class Helpers:
    def getAlphaChannel(texture):
        img = Image.open('input//' + texture)
        if img.info.get("transparency", None) is not None:
            return True
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True
        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True
        return False

    def getTextureSize(texture):
        TextureData = Image.open('input//' + texture)
        imWidth, imHeight = TextureData.size
        return imWidth, imHeight

    def createFolder(dir_name):
        os.makedirs(dir_name, exist_ok=True)

class Tools:
    def rdfGenerator(texture, format, width, height):
        arq = open("temp//" + texture.replace('.png', '.rdf'), 'w', encoding='utf-8')
        arq.write('''<?xml version="1.0" encoding="utf-8" ?>
        <RDF Version="XPR2">
            <Texture
            Name   = "StrName"
            Source = "''' + str(texture.replace('.png', '.tga')) + '''"
            Format = "''' + format + '''"
            Width  = "''' + str(width) + '''"
            Height = "''' + str(height) +'''"
            Levels = "1"
            />
        </RDF>
        ''')
        arq.close()

    def texture2tga(texture):
        TextureData = Image.open('input//' + texture)
        TextureData.save('temp//' + texture.replace('.png', '.tga'))

    def texture2dds(texture):
        if Helpers.getAlphaChannel(texture) == True:
            subprocess.check_call('quicktex encode bc3 --no-flip input//' + texture + ' -o temp//', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif Helpers.getAlphaChannel(texture) == False:
            subprocess.check_call('quicktex encode bc1 --no-flip input//' + texture + ' -o temp//', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)