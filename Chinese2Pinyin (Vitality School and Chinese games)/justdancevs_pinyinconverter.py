import os
import sys
import json
import time
import pinyin_jyutping_sentence
import unidecode
from tkinter import *
from tkinter import filedialog
import pathlib

openFile = Tk()
openFile.title('')

# Just Dance: Vitality School Pinyin Converter tool (Release Candidate #1)
# Credits: WodsonKun, augustodoidin (base code)

mainjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your JSON", filetypes=[("Just Dance: Vitality School JSON (.json)", "*.json")] )

# JSON principal
with open(mainjson, "r", encoding='utf-8-sig') as raw:
    jsonMainData = json.load(raw)

# Lê a base do JSON, assim já define coisas como Artista e nome da música
jsonMapName = jsonMainData['MapName']
jsonArtist = jsonMainData['Artist']
jsonTitle = jsonMainData['Title']
jsonCredits = jsonMainData['Credits']
jsonNumCoach = jsonMainData['NumCoach']
jsonLyricsColor = jsonMainData['lyricsColor']
jsonVideoOffset = jsonMainData['videoOffset']
jsonBeatData = jsonMainData['beats']

# Lê os valores das lyrics (para serem modificados depois)
jsonLyricData = jsonMainData['lyrics']

# Lê os valores dos pictos (para serem modificados depois)
jsonPictoData = jsonMainData['pictos']

# Total de lyrics e pictos (importante)
totalLyrics = len(jsonLyricData) + 1
totalPictos = len(jsonPictoData) + 1

# Variáveis de indexação (precisa também)
cL = 0
cP = 0

# Lê as informações de AudioPreview (resumindo, coisa que o JSON2DTAPE vai precisar pro musictrack)
jsonPreviewData = jsonMainData['AudioPreview']
jsonLoopStartData = jsonPreviewData['loopStart']
jsonOffsetData = jsonPreviewData['offset']

# Começa a escrever a base do JSON
arq = open("output" + "//" + jsonMapName.lower() + "_pinyin.json", "w", encoding='utf-8')
arq.write('{')
arq.write('"MapName": "' + jsonMapName + '",')
arq.write('"JDVersion": 2017,')
arq.write('"OriginalJDVersion": 4514,')
arq.write('"Artist": "' + jsonArtist + '",')
arq.write('"Title": "' + jsonTitle + '",')
arq.write('"Credits": "' + jsonCredits + '",')
arq.write('"NumCoach": ')
if (jsonNumCoach == "Solo"):
    arq.write(str(1))
elif (jsonNumCoach == "Duo"):
    arq.write(str(2))
elif (jsonNumCoach == "Trio"):
    arq.write(str(3))
elif (jsonNumCoach == "Quartet"):
    arq.write(str(4))
arq.write(',')
arq.write('"CountInProgression": 1,')
arq.write('"DancerName": "Unknown Dancer",')
arq.write('"LocaleID": 4294967295,')
arq.write('"MojoValue": 0,')
arq.write('"Mode": 6,')
arq.write('"Status": 3,')
arq.write('"LyricsType": 0,')
arq.write('"BackgroundType": 0,')
arq.write('"Difficulty": 2,')
arq.write('"MojoValue": 0,')
arq.write('"DefaultColors": {')
arq.write('"lyrics": "0xFFFFFFFF",')
arq.write('"theme": "0xFFFFFFFF",')
arq.write('"songcolor_1A": "0xFFFFFFFF",')
arq.write('"songcolor_1B": "0xFFFFFFFF",')
arq.write('"songcolor_2A": "0xFFFFFFFF",')
arq.write('"songcolor_2B": "0xFFFFFFFF"')
arq.write('},')
arq.write('"lyricsColor": "' + jsonLyricsColor + '",')
arq.write('"videoOffset": ' + str(jsonVideoOffset) + ',')
arq.write('"beats": ' + str(jsonBeatData) + ',')
arq.write('"lyrics": [')

ly_running = True
cL = 1

while ly_running:
    if cL + 1 == totalLyrics:
        ly_running = False

    if cL < totalLyrics:
        arq.write('{')
        arq.write('"time": ' + str(jsonLyricData[cL - 1]['time']) + ',')
        arq.write('"duration": ' + str(jsonLyricData[cL - 1]['duration']) + ',')
        arq.write('"text": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[cL - 1]['text'])).replace(' ', '') + ' ",')
        arq.write('"isLineEnding": ' + str(jsonLyricData[cL - 1]['isLineEnding']))
        arq.write('},')
    if cL == (totalLyrics - 1):
        arq.write('{')
        arq.write('"time": ' + str(jsonLyricData[cL - 1]['time']) + ',')
        arq.write('"duration": ' + str(jsonLyricData[cL - 1]['duration']) + ',')
        arq.write('"text": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[cL - 1]['text'])).replace(' ', '') + ' ",')
        arq.write('"isLineEnding": ' + str(jsonLyricData[cL - 1]['isLineEnding']))
        arq.write('}')
                
    cL += 1

arq.write('],')
arq.write('"pictos": [')

pic_running = True
cP = 1
    
while pic_running:
    if cP + 1 == totalPictos:
        pic_running = False

    if cP < totalPictos:
        arq.write('{')
        arq.write('"time": ' + str(jsonPictoData[cP - 1]['time']) + ',')
        arq.write('"duration": ' + str(jsonPictoData[cP - 1]['duration']) + ',')
        arq.write('"name": "' + jsonPictoData[cP - 1]['name'] + '"')
        arq.write('},')
    if cP == (totalPictos - 1):
        arq.write('{')
        arq.write('"time": ' + str(jsonPictoData[cP - 1]['time']) + ',')
        arq.write('"duration": ' + str(jsonPictoData[cP - 1]['duration']) + ',')
        arq.write('"name": "' + jsonPictoData[cP - 1]['name'] + '"')
        arq.write('}')
                
    cP += 1

arq.write('],')
arq.write('"AudioPreview": {')
arq.write('"coverflow": {')
arq.write('"startbeat": ' + str(jsonLoopStartData))
arq.write('},')
arq.write('"prelobby": {')
arq.write('"startbeat": ' + str(jsonLoopStartData))
arq.write('}')
arq.write('},')
arq.write('"AudioPreviewFadeTime": ' + str(int(jsonOffsetData)))
arq.write('}')
arq.close()