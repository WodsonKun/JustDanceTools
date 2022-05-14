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
jsonMapName = mainKTAPE["MapName"]

# Gets "Clips" data from the KTAPE
KTAPEClipsData = mainKTAPE["Clips"]

# Começa a escrever o KTAPE (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
arq = open("output" + "//" + jsonMapName.lower() + "_tml_karaoke.ktape.ckd", "w", encoding='utf-8')

# Escreve o header do KTAPE
arq.write('{"__class": "Tape","Clips": ')

# Escreve os clips do KTAPE
i = 0
clips = '['

while i < len(mainKTAPE["Clips"][1:-1]):
    result = kks.convert((KTAPEClipsData[i]['Lyrics']))
    clips = clips + '{"__class": "KaraokeClip",'
    clips = clips + '"Id": ' + str(KTAPEClipsData[i]['Id']) + ','
    clips = clips + '"TrackId": ' + str(KTAPEClipsData[i]['TrackId']) + ','
    clips = clips + '"IsActive": ' + str(KTAPEClipsData[i]['IsActive']) + ','
    clips = clips + '"StartTime": ' + str(KTAPEClipsData[i]['StartTime']) + ','
    clips = clips + '"Duration": ' + str(KTAPEClipsData[i]['Duration']) + ','
    clips = clips + '"Pitch": ' + str(KTAPEClipsData[i]['Pitch']) + ','
    clips = clips + '"Lyrics": "'
    if (KTAPEClipsData[i - 1]['IsEndOfLine'] == 1): 
        for item in result:
            clips = clips + item['hepburn'].capitalize()
        clips = clips + ' ",'
    elif (KTAPEClipsData[i]['IsEndOfLine'] == 1): 
        for item in result:
            clips = clips + item['hepburn']
        clips = clips + '",'
    else:
        for item in result:
            clips = clips + item['hepburn']
        clips = clips + ' ",'
    clips = clips + '"IsEndOfLine": ' + str(KTAPEClipsData[i]['IsEndOfLine']) + ','
    clips = clips + '"ContentType": ' + str(KTAPEClipsData[i]['ContentType']) + ','
    clips = clips + '"StartTimeTolerance": ' + str(KTAPEClipsData[i]['StartTimeTolerance']) + ','
    clips = clips + '"EndTimeTolerance": ' + str(KTAPEClipsData[i]['EndTimeTolerance']) + ','
    clips = clips + '"SemitoneTolerance": ' + str(KTAPEClipsData[i]['SemitoneTolerance']) + '}'
    clips = clips + ','
    
    i += 1

clips = clips + ']'
clips = clips.replace(",]","]")
arq.write(clips)
    
# Escreve o footer do KTAPE
arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')

# Fecha o arquivo
arq.close()

