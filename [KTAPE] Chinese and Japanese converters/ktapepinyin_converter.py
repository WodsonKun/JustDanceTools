import sys, io, unidecode, json, pathlib
from tkinter import *
from tkinter import filedialog

# Importa o Jyutping, para ser possível converter os KTAPEs para PinYin
text_trap = io.StringIO()
sys.stderr = text_trap
import pinyin_jyutping_sentence
sys.stderr = sys.__stderr__

# Initializes tkinter
openFile = Tk()
openFile.title('')

# WodsonKun's KTAPE PinYin converter
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
    clips = clips + '{"__class": "KaraokeClip",'
    clips = clips + '"Id": ' + str(KTAPEClipsData[i]['Id']) + ','
    clips = clips + '"TrackId": ' + str(KTAPEClipsData[i]['TrackId']) + ','
    clips = clips + '"IsActive": ' + str(KTAPEClipsData[i]['IsActive']) + ','
    clips = clips + '"StartTime": ' + str(KTAPEClipsData[i]['StartTime']) + ','
    clips = clips + '"Duration": ' + str(KTAPEClipsData[i]['Duration']) + ','
    clips = clips + '"Pitch": ' + str(KTAPEClipsData[i]['Pitch']) + ','
    if (KTAPEClipsData[i - 1]['IsEndOfLine'] == 1): 
        clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(KTAPEClipsData[i]['Lyrics'])).capitalize() + ' ",'
    elif (KTAPEClipsData[i]['IsEndOfLine'] == 1): 
        clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(KTAPEClipsData[i]['Lyrics'])) + '",'
    else:
        clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(KTAPEClipsData[i]['Lyrics'])) + ' ",'
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