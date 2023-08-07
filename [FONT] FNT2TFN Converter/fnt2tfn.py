import os, sys, io, json, xmltodict, pathlib, shutil
from tkinter import *
from tkinter import filedialog

# Woody's BFFont FNT to TFN converter
## Creates a "output" folder
os.makedirs('output\\', exist_ok = True)

# Initializes Tkinter (to use the file picker)
openFile = Tk()
openFile.title('')

# Searches for each bundle
fontXML = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your .fnt file", filetypes=[("FNT XML", "*.fnt")] )
    
# Destroys the actual Tkinter instance
openFile.destroy()

# Parse the XML file as a dict (easier to use)
with open(fontXML) as fd:
    doc = xmltodict.parse(fd.read())

# Get the 'info'
xmlFace = doc['font']['info']['@face']
xmlSize = doc['font']['info']['@size']

# Get the 'common' info
xmlLineHeight = doc['font']['common']['@lineHeight']
xmlBase = doc['font']['common']['@base']
xmlScaleW = doc['font']['common']['@scaleW']
xmlScaleH = doc['font']['common']['@scaleH']

# Writes the header of the TFN
arq = open('output\\' + os.path.basename(fontXML).replace(".fnt", "") + '.tfn.ckd', "w")
arq.write('{"__class": "FontTemplate","info": {"__class": "Info","face": "' + str(xmlFace) + '","size": ' + str(xmlSize) + ',"bold": 0,"italic": 0,"charset": "","unicode": 1,"stretchH": 100,"smooth": 1,"aa": 1,"paddingLeft": 4,"paddingRight": 4,"paddingTop": 4,"paddingBottom": 4,"spacingLeft": 2,"spacingTop": 2,"outline": 0},')

# Writes the "common" section of the TFN
arq.write('"common": {"__class": "Common","lineHeight": ' + str(xmlLineHeight) + ',"base": ' + str(xmlBase) + ', "scaleW": ' + str(xmlScaleW) + ',"scaleH": ' + str(xmlScaleH) + '},')

# Writes the "pages" section of the TFN
arq.write('"pages": ')
clips = '['

# Writes "Page" clips
if (isinstance(doc['font']['pages']['page'], list)): # If it is a list (has more than one page entry...)
    for page in range(len(doc['font']['pages']['page'])):
        pagePage = int(doc['font']['pages']['page'][page]['@id']) + 2
        clips += ('{"__class": "Page","id": ' + str(pagePage) + ', "file": "world/ui/fonts/' + str(doc['font']['pages']['page'][page]['@file']).replace(".png", ".tga") + '"},')
elif (isinstance(doc['font']['pages']['page'], dict)): # Else, if it is a dict (has only one page entry...)
    clips += ('{"__class": "Page","id": ' + str(doc['font']['pages']['page']['@id']) + ', "file": "world/ui/fonts/' + str(doc['font']['pages']['page']['@file']).replace(".png", ".tga") + '"},')

clips += ']'
clips = clips.replace(",]","]")
arq.write(clips)

# Writes the "chars" section of the TFN
arq.write(',"chars": ')
clips = '['

for char in range(len(doc['font']['chars']['char'])):
    
    # Gets the info for every character
    charId = doc['font']['chars']['char'][char]['@id']
    charX = doc['font']['chars']['char'][char]['@x']
    charY = doc['font']['chars']['char'][char]['@y']
    charWidth = doc['font']['chars']['char'][char]['@width']
    charHeight = doc['font']['chars']['char'][char]['@height']
    charXOffset = doc['font']['chars']['char'][char]['@xoffset']
    charYOffset = doc['font']['chars']['char'][char]['@yoffset']
    charXAdvance = doc['font']['chars']['char'][char]['@xadvance']
    charPage = int(doc['font']['chars']['char'][char]['@page']) + 2
    charChannel = doc['font']['chars']['char'][char]['@chnl']
    
    # Writes 'Char' clips
    clips += '{"__class": "Char", "id": ' + str(charId) + ',"x": ' + str(charX) + ',"y": ' + str(charY) + ',"width": ' + str(charWidth) + ',"height": ' + str(charHeight) + ',"xoffset": ' + str(charXOffset) + ',"yoffset": ' + str(charYOffset) + ',"xadvance": ' + str(charXAdvance) + ',"page": ' + str(charPage) + ',"chnl": ' + str(charChannel)
    clips += '},'
    
# Writes the footer of the TFN
clips += ']'
clips = clips.replace(",]","]")
arq.write(clips)
arq.write('}')