import sys
import pykakasi
import unidecode
import json
from tkinter import *
from tkinter import filedialog
import pathlib

# Initializes tkinter
openFile = Tk()
openFile.title('')

# Initializes pykakasi
kks = pykakasi.kakasi()

# WodsonKun's KTAPE Kanji to Romaji converter
# Credits to... Me?

mainjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your KTAPE", filetypes=[("KTAPE (.ktape.ckd)", "*.ckd")] )

# JSON principal
with open(mainjson, "r", encoding='utf-8-sig') as raw:
    mainKTAPE = json.load(raw)

# Gets the codename from the KTAPE
mapName = mainKTAPE["MapName"]

# Gets "Clips" data from the KTAPE
KTAPEClipsData = mainKTAPE["Clips"]

# Gets the total length of Clips inside of the KTAPE
totalClips = len(KTAPEClipsData) + 1

# Starts writing the new KTAPE
arq = open("output" + "//" + mapName.lower() + "_tml_karaoke.ktape.ckd", "w", encoding='utf-8')

arq.write('{')
arq.write('"__class": "Tape",')
arq.write('"Clips": [')

ly_running = True
cL = 1

while ly_running:
    if cL + 1 == totalClips:
        ly_running = False

    if cL < totalClips:
        result = kks.convert((KTAPEClipsData[cL - 1]['Lyrics']))
        arq.write('{')
        arq.write('"__class": "KaraokeClip",')
        arq.write('"Id": ' + str(KTAPEClipsData[cL - 1]['Id']) + ',')
        arq.write('"TrackId": ' + str(KTAPEClipsData[cL - 1]['TrackId']) + ',')
        arq.write('"IsActive": ' + str(KTAPEClipsData[cL - 1]['IsActive']) + ',')
        arq.write('"StartTime": ' + str(KTAPEClipsData[cL - 1]['StartTime']) + ',')
        arq.write('"Duration": ' + str(KTAPEClipsData[cL - 1]['Duration']) + ',')
        arq.write('"Pitch": ' + str(KTAPEClipsData[cL - 1]['Pitch']) + ',')
        arq.write('"Lyrics": "')
        for item in result:
            arq.write(item['hepburn'])
        arq.write(' ",') 
        arq.write('"IsEndOfLine": ' + str(KTAPEClipsData[cL - 1]['IsEndOfLine']) + ',')
        arq.write('"ContentType": ' + str(KTAPEClipsData[cL - 1]['ContentType']) + ',')
        arq.write('"StartTimeTolerance": ' + str(KTAPEClipsData[cL - 1]['StartTimeTolerance']) + ',')
        arq.write('"EndTimeTolerance": ' + str(KTAPEClipsData[cL - 1]['EndTimeTolerance']) + ',')
        arq.write('"SemitoneTolerance": ' + str(KTAPEClipsData[cL - 1]['SemitoneTolerance']))
        arq.write('},')
    if cL == (totalClips - 1):
        result = kks.convert((KTAPEClipsData[cL - 1]['Lyrics']))
        arq.write('{')
        arq.write('"__class": "KaraokeClip",')
        arq.write('"Id": ' + str(KTAPEClipsData[cL - 1]['Id']) + ',')
        arq.write('"TrackId": ' + str(KTAPEClipsData[cL - 1]['TrackId']) + ',')
        arq.write('"IsActive": ' + str(KTAPEClipsData[cL - 1]['IsActive']) + ',')
        arq.write('"StartTime": ' + str(KTAPEClipsData[cL - 1]['StartTime']) + ',')
        arq.write('"Duration": ' + str(KTAPEClipsData[cL - 1]['Duration']) + ',')
        arq.write('"Pitch": ' + str(KTAPEClipsData[cL - 1]['Pitch']) + ',')
        arq.write('"Lyrics": "')
        for item in result:
            arq.write(item['hepburn'])
        arq.write('",') 
        arq.write('"IsEndOfLine": ' + str(KTAPEClipsData[cL - 1]['IsEndOfLine']) + ',')
        arq.write('"ContentType": ' + str(KTAPEClipsData[cL - 1]['ContentType']) + ',')
        arq.write('"StartTimeTolerance": ' + str(KTAPEClipsData[cL - 1]['StartTimeTolerance']) + ',')
        arq.write('"EndTimeTolerance": ' + str(KTAPEClipsData[cL - 1]['EndTimeTolerance']) + ',')
        arq.write('"SemitoneTolerance": ' + str(KTAPEClipsData[cL - 1]['SemitoneTolerance']))
        arq.write('}')
                
    cL += 1
    
arq.write('],')
arq.write('"TapeClock": 0,')
arq.write('"TapeBarCount": 1,')
arq.write('"FreeResourcesAfterPlay": 0,')
arq.write('"MapName": "' + mapName + '",')
arq.write('"SoundwichEvent": ""')
arq.write('}')