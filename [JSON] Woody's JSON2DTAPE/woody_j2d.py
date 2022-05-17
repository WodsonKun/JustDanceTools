# Importar dependências necessárias
import os, io, sys, json, time, math, unidecode, pathlib, random, numpy, shutil, subprocess
from tkinter import *
from tkinter import filedialog
from PIL import Image

# Importa o Jyutping, para ser possível converter os KTAPEs para PinYin
text_trap = io.StringIO()
sys.stderr = text_trap
import pinyin_jyutping_sentence
sys.stderr = sys.__stderr__

## Funções que facilitam a conversão dos JSONs para TAPEs
# hex2RGB (por Julian White | https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python)
def hex2RGB(value):
    try:
        value = value.lstrip('#') # Remove o "#" do valor HEX para conversão
    except:
        value = value.lstrip('0xFF') # Se "#" não encontrado, tenta remover "0xFF", também encontrado nas JSONs
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)) # Retorna o valor em RGB

# randomId (por WodsonKun)
def randomId():
    return math.floor(random.randint(0, 40000) * (400000 - 100000 + 1) + 100000) # Gera um valor randômico e retorna o mesmo para ser usado como ID

# ubiArtTime (por: planedec50, WodsonKun)
def ubiArtTime(jsonTimeValue, parse):
    if (genNewBeats == "y") or (genNewBeats == "Y"): # Se novas beats tenham sido geradas...
        if bool(parse):
            return int(numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0)) # Caso seja "verdadeiro", ele faz a interpolação dos valores e retorna os mesmos
        elif not bool(parse):
            return numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0) 
    if (genNewBeats == "n") or (genNewBeats == "N"):
        if bool(parse):
            return int(numpy.interp(jsonTimeValue, jsonBeatData, BeatsMap24, 0))
        elif not bool(parse):
            return numpy.interp(jsonTimeValue, jsonBeatData, BeatsMap24, 0)
    
# createOutputDir (by: WodsonKun)
def createOutputDir():
    try:
        os.mkdir("output//" + jsonMapName) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada

########################################################################## WodsonKun's JSON2DTAPE (v1.1.5) #########################################################################
######################################################################## Créditos a planedec50, augustodoidin ######################################################################

### Cria um songdesc através de um JSON (funciona com todos os tipos)
def SongDescJ2D():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    mainjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
    
    # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Lê os campos necessários do JSON para geração da songdesc (caso os valores não sejam encontrados, ele pergunta por valores do usuário e define valores padrão para os outros)
    jsonMapName = jsonMainData['MapName']
    jsonArtist = jsonMainData['Artist']
    jsonTitle = jsonMainData['Title']
    try:
        jsonCredits = jsonMainData['Credits']
    except:
        jsonCredits = "CREDITS STRING TO BE FILLED"
    try:
        jsonNumCoach = jsonMainData['NumCoach']
    except:
        jsonNumCoach = int(input('Digite o número de coaches: '))
    try:
        jsonDifficulty = jsonMainData['Difficulty']
    except:
        jsonDifficulty = int(input('Digite a dificuldade da música (1, 2, 3 or 4): '))
    try:
        jsonOriginalJDVersion = jsonMainData['OriginalJDVersion']
    except: 
        jsonOriginalJDVersion = 9999
    try:
        jsonLocaleID = jsonMainData['LocaleID']
    except:
        jsonLocaleID = 4294967295
    
    # Lê cores de letras e banners (e de novo, caso não encontrados, definem um valor padrão)
    jsonLyricsColor = jsonMainData['lyricsColor']
    try:
        json1AColor = jsonMainData['DefaultColors']['songColor_1A']
    except:
        json1AColor = "0xFF444444"
    try:
        json1BColor = jsonMainData['DefaultColors']['songColor_1B']
    except:
        json1BColor = "0xFF111111"
    try:
        json2AColor = jsonMainData['DefaultColors']['songColor_2A']
    except:
        json2AColor = "0xFFAAAAAA"
    try:
        json2BColor = jsonMainData['DefaultColors']['songColor_2B']
    except:
        json2BColor = "0xFF777777"
    
    # Cria a pasta com o codenome da música
    createOutputDir()
    
    # Começa a escrever a songdesc (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
    arq = open("output" + "//" + jsonMapName + "//songdesc.tpl.ckd", "w", encoding='utf-8')
    arq.write('{"__class": "Actor_Template","WIP": 0,"LOWUPDATE": 0,"UPDATE_LAYER": 0,"PROCEDURAL": 0,"STARTPAUSED": 0,"FORCEISENVIRONMENT": 0,"COMPONENTS": [{"__class": "JD_SongDescTemplate","MapName": "' + jsonMapName + '","JDVersion": 2017,"OriginalJDVersion": ' + str(jsonOriginalJDVersion) + ',"Artist": "' + jsonArtist + '","DancerName": "Unknown Dancer","Title": "' + jsonTitle + '","Credits": "' + jsonCredits + '","PhoneImages": {')
    arq.write('"Cover": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_cover_phone.jpg",')
    if (jsonNumCoach == "Solo" or jsonNumCoach == 1):
        arq.write('"coach1": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_1_phone.png"')
    elif (jsonNumCoach == "Duo" or jsonNumCoach == 2):
        arq.write('"coach1": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_2_phone.png"')
    elif (jsonNumCoach == "Trio" or jsonNumCoach == 3):
        arq.write('"coach1": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_3_phone.png"')
    elif (jsonNumCoach == "Quartet" or jsonNumCoach == 4):
        arq.write('"coach1": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_3_phone.png", "coach4": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_4_phone.png"')
    arq.write('},')
    if (jsonNumCoach == "Solo" or jsonNumCoach == 1):
        arq.write('"NumCoach": ' + str(1) + ',')
    elif (jsonNumCoach == "Duo" or jsonNumCoach == 2):
        arq.write('"NumCoach": ' + str(2) + ',')
    elif (jsonNumCoach == "Trio" or jsonNumCoach == 3):
        arq.write('"NumCoach": ' + str(3) + ',')
    elif (jsonNumCoach == "Quartet" or jsonNumCoach == 4):
        arq.write('"NumCoach": ' + str(4) + ',')
    arq.write('"MainCoach": -1,')
    if (jsonDifficulty == "Easy" or jsonDifficulty == 1):
        arq.write('"Difficulty": ' + str(1) + ',')
    elif (jsonDifficulty == "Normal" or jsonDifficulty == 2):
        arq.write('"Difficulty": ' + str(2) + ',')
    elif (jsonDifficulty == "Hard" or jsonDifficulty == 3):
        arq.write('"Difficulty": ' + str(3) + ',')
    elif (jsonDifficulty == "Extreme" or jsonDifficulty == 4):
        arq.write('"Difficulty": ' + str(4) + ',')
    if (jsonDifficulty == "Easy" or jsonDifficulty == 1):
        arq.write('"Energy": ' + str(0) + ',')
    elif (jsonDifficulty == "Normal" or jsonDifficulty == 2):
        arq.write('"Energy": ' + str(1) + ',')
    elif (jsonDifficulty == "Hard" or jsonDifficulty == 3):
        arq.write('"Energy": ' + str(2) + ',')
    elif (jsonDifficulty == "Extreme" or jsonDifficulty == 4):
        arq.write('"Energy": ' + str(3) + ',')
    arq.write('"backgroundType": 0,"LyricsType": 0,"Tags": ["main"],"Status": 3,"LocaleID": ' + str(jsonLocaleID) + ',"MojoValue": 0,"CountInProgression": 1,"DefaultColors":{"songcolor_2a": [1, ' + str(hex2RGB(json2AColor)[0]/255) + ', ' +  str(hex2RGB(json2AColor)[1]/255) + ', ' +  str(hex2RGB(json2AColor)[2]/255) + '], "lyrics": [1, ' + str(hex2RGB(jsonLyricsColor)[0]/255) + ', ' +  str(hex2RGB(jsonLyricsColor)[1]/255) + ', ' +  str(hex2RGB(jsonLyricsColor)[2]/255) + '], "theme": [1, 1, 1, 1],"songcolor_1a": [1, ' + str(hex2RGB(json1AColor)[0]/255) + ', ' +  str(hex2RGB(json1AColor)[1]/255) + ', ' +  str(hex2RGB(json1AColor)[2]/255) + '],"songcolor_2b": [1, ' + str(hex2RGB(json2BColor)[0]/255) + ', ' +  str(hex2RGB(json2BColor)[1]/255) + ', ' +  str(hex2RGB(json2BColor)[2]/255) + '],"songcolor_1b": [1, ' + str(hex2RGB(json1BColor)[0]/255) + ', ' +  str(hex2RGB(json1BColor)[1]/255) + ', ' +  str(hex2RGB(json1BColor)[2]/255) + ']},"Paths": {"Avatars": null,"AsyncPlayers": null}}]}')
    
    # Fecha o arquivo
    arq.close()
    
# Gera um KTAPE através de um JSON (todos funcionam)
def KTAPEJ2D():
    # Pergunta se é um JSON do Vitality School
    QPinYin = input(str("Se for um JSON do Vitality School, deseja converter o KTAPE para PinYin? (Isso os torna legíveis para a Old Gen): "))
        
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal
    mainjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your JSON", filetypes=[("Just Dance: Vitality School JSON (.json)", "*.json")] )
    
    # Lê o JSON principal
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
        
    # Destrói a instância do Tkinter
    openFile.destroy()
    
    # Lê os campos necessários para gerar o KTAPE
    jsonMapName = jsonMainData['MapName']
    jsonBeatData = jsonMainData['beats']
    jsonLyricData = jsonMainData['lyrics']
    
    # Cria a pasta com o codenome da música
    createOutputDir()
    
    # Cria um array para guardar as beats emendadas
    BeatsMap24 = []
    
    # Pergunta se quer converter as beats
    genNewBeats = input(str("Você quer gerar beats novas? (Y ou N): "))
    if (genNewBeats == "y") or (genNewBeats == "Y"):
        NewBeats = []
        bpm = float(input("Insira o BPM da música: "))
        beat = int(round(60000/bpm))
        gerados = 0
        quantidade = len(jsonBeatData)
        while (gerados <= quantidade):
            if gerados == quantidade:
                gerados = gerados +1
                NewBeats.append(beat*gerados)
            else:
                gerados = gerados +1
                NewBeats.append(beat*gerados)
        
        if (len(NewBeats) > 5 and NewBeats[0] != 0):
            NewBeats.insert(0, 0)
            firstBeat = NewBeats[0]
            nextBeats = NewBeats[0:5]
            i = 0
            while (i < 5):
                try:
                    NewBeats[i:nextBeats[i] - firstBeat]
                finally:
                    i+=1

        i = 0
        while (i < len(NewBeats)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1
                
    elif (genNewBeats == "n") or (genNewBeats == "N"):
        if (len(jsonBeatData) > 5 and jsonBeatData[0] != 0):
            jsonBeatData.insert(0, 0)
            firstBeat = jsonBeatData[0]
            nextBeats = jsonBeatData[0:5]
            i = 0
            while (i < 5):
                try:
                    jsonBeatData[i:nextBeats[i] - firstBeat]
                finally:
                    i+=1

        i = 0
        while (i < len(jsonBeatData)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1
    
    # Começa a escrever o KTAPE (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
    arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_tml_karaoke.ktape.ckd", "w", encoding='utf-8')
    
    # Escreve o header do KTAPE
    arq.write('{"__class": "Tape","Clips": ')
    
    # Escreve os clips do KTAPE
    i = 0
    clips = '['
    while i < len(jsonMainData['lyrics'][1:-1]):
        clips = clips + '{"__class": "KaraokeClip","Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
        clips = clips + str(ubiArtTime(jsonLyricData[i]['time'], True))
        clips = clips + ',"Duration": '
        clips = clips + str(ubiArtTime(jsonLyricData[i]['duration'], True))
        if (QPinYin == "Y") or (QPinYin == "y"):
            if (jsonLyricData[i - 1]['isLineEnding'] == 1): 
                clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[i]['text'])).capitalize() + ' ","IsEndOfLine": '
            elif (jsonLyricData[i]['isLineEnding'] == 1): 
                clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[i]['text'])) + '","IsEndOfLine": '
            else:
                clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[i]['text'])) + ' ","IsEndOfLine": '
        if (QPinYin == "N") or (QPinYin == "n"):
            clips = clips + ',"Pitch": 8.661958,"Lyrics": "' + jsonLyricData[i]['text'] + '","IsEndOfLine": '
        try:
            clips = clips + str(jsonLyricData[i]['isLineEnding'])
        except KeyError:
            clips = clips + '0'
        clips = clips + ',"ContentType": 0,"StartTimeTolerance": 4,"EndTimeTolerance": 4,"SemitoneTolerance": 5}'
        clips = clips + ','
        i += 1
    clips = clips + ']'
    clips = clips.replace(",]","]")
    arq.write(clips)
    
    # Escreve o footer do KTAPE
    arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
    
    # Fecha o arquivo
    arq.close()

# Gera um DTAPE através do JSON principal e dos JSONs de moves
def DTAPEJ2D():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal
    mainjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your JSON", filetypes=[("Just Dance: Vitality School JSON (.json)", "*.json")] )
    
    # Abre e lê o JSON principal
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
        
    # Destrói a instância do Tkinter
    openFile.destroy()
    
    # Lê os campos necessários para gerar o DTAPE
    jsonMapName = jsonMainData['MapName']
    try:
        jsonNumCoach = jsonMainData['NumCoach']
    except:
        jsonNumCoach = int(input('Type the number of coaches: '))
    jsonBeatData = jsonMainData['beats']
    jsonPictoData = jsonMainData['pictos']
    totalPictos = len(jsonPictoData)
    
    # Cria a pasta com o codenome da música
    createOutputDir()
    
    # Cria um array para guardar as beats emendadas
    BeatsMap24 = []
    
    # Pergunta se quer converter as beats
    genNewBeats = input(str("Você quer gerar beats novas? (Y ou N): "))
    if (genNewBeats == "y") or (genNewBeats == "Y"):
        NewBeats = []
        bpm = float(input("Insira o BPM da música: "))
        beat = int(round(60000/bpm))
        gerados = 0
        quantidade = len(jsonBeatData)
        while (gerados <= quantidade):
            if gerados == quantidade:
                gerados = gerados +1
                NewBeats.append(beat*gerados)
            else:
                gerados = gerados +1
                NewBeats.append(beat*gerados)
        
        if (len(NewBeats) > 5 and NewBeats[0] != 0):
            NewBeats.insert(0, 0)
            firstBeat = NewBeats[0]
            nextBeats = NewBeats[0:5]
            i = 0
            while (i < 5):
                try:
                    NewBeats[i:nextBeats[i] - firstBeat]
                finally:
                    i+=1

        i = 0
        while (i < len(NewBeats)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1
                
    elif (genNewBeats == "n") or (genNewBeats == "N"):
        if (len(jsonBeatData) > 5 and jsonBeatData[0] != 0):
            jsonBeatData.insert(0, 0)
            firstBeat = jsonBeatData[0]
            nextBeats = jsonBeatData[0:5]
            i = 0
            while (i < 5):
                try:
                    jsonBeatData[i:nextBeats[i] - firstBeat]
                finally:
                    i+=1

        i = 0
        while (i < len(jsonBeatData)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1
    
    # Começa a escrever o DTAPE (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
    arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_tml_dance.dtape.ckd", "w", encoding='utf-8')
    
    # Escreve o header do DTAPE
    arq.write('{"__class": "Tape","Clips": ')
    
    # Escreve os clips do DTAPE   
    # Checa quantos coaches a música tem e caso tenha um, converte seus moves
    if (jsonNumCoach == "Solo" or jsonNumCoach == 1):
    
        # Inicializa o Tkinter (para pegar os JSONs usando o seletor de arquivos)
        openFile = Tk()
        openFile.title('')
        
        # Procura os JSONs de Moves0 e Moves1
        Moves0JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        
        # Lê os JSONs de Moves0 e Moves1
        with open(Moves0JSON, "r", encoding='utf-8') as raw:
            jsonMoves0Data = json.load(raw)
        
        # Destrói a instância do Tkinter ()
        openFile.destroy()
        
        # Inicia os clips
        dclips = '['
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips = dclips + '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips = dclips + ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips = dclips + ','
            
            # Aumenta o valor de "i"
            i += 1
        
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
            
    # Checa quantos coaches a música tem, e caso tenha dois coaches, procura por seus moves e os converte
    if (jsonNumCoach == "Duo" or jsonNumCoach == 2):
    
        # Inicializa o Tkinter (para pegar os JSONs usando o seletor de arquivos)
        openFile = Tk()
        openFile.title('')
        
        # Procura os JSONs de Moves0 e Moves1
        Moves0JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        Moves1JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves1 JSON (.json)", "*.json")] )
        
        # Lê os JSONs de Moves0 e Moves1
        with open(Moves0JSON, "r", encoding='utf-8') as raw:
            jsonMoves0Data = json.load(raw)
        with open(Moves1JSON, "r", encoding='utf-8') as raw:
            jsonMoves1Data = json.load(raw)
        
        # Destrói a instância do Tkinter ()
        openFile.destroy()
        
        # Inicia os clips
        dclips = '['
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves1Data[i]['name'] + '.msm", '
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json1GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 1, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips = dclips + '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips = dclips + ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips = dclips + ','
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
        
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                if (json1GoldMove != "") or (json1GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
    
    # Checa quantos coaches a música tem, e caso tenha três coaches, procura por seus moves e os converte
    if (jsonNumCoach == "Trio" or jsonNumCoach == 3):
    
        # Inicializa o Tkinter (para pegar os JSONs usando o seletor de arquivos)
        openFile = Tk()
        openFile.title('')
        
        # Procura os JSONs de Moves0, Moves1 e Moves2
        Moves0JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        Moves1JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves1 JSON (.json)", "*.json")] )
        Moves2JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves2 JSON (.json)", "*.json")] )
        
        # Lê os JSONs de Moves0 e Moves1
        with open(Moves0JSON, "r", encoding='utf-8') as raw:
            jsonMoves0Data = json.load(raw)
        with open(Moves1JSON, "r", encoding='utf-8') as raw:
            jsonMoves1Data = json.load(raw)
        with open(Moves2JSON, "r", encoding='utf-8') as raw:
            jsonMoves2Data = json.load(raw)
        
        # Destrói a instância do Tkinter ()
        openFile.destroy()
        
        # Inicia os clips
        dclips = '['
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves1Data[i]['name'] + '.msm", '
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json1GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 1, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 3
        i = 0
        while i < len(jsonMoves2Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves2Data[i]['name'] + '.msm", '
            try:
                json2GoldMove = jsonMoves2Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json2GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 2, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips = dclips + '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips = dclips + ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips = dclips + ','
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
        
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                if (json1GoldMove != "") or (json1GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 3
        i = 0
        while i < len(jsonMoves2Data[1:-1]):
            try:
                json2GoldMove = jsonMoves2Data[i]['goldMove']
                if (json2GoldMove != "") or (json2GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
    
    # Checa quantos coaches a música tem, e caso tenha quatro coaches, procura por seus moves e os converte
    if (jsonNumCoach == "Quartet" or jsonNumCoach == 4):
    
        # Inicializa o Tkinter (para pegar os JSONs usando o seletor de arquivos)
        openFile = Tk()
        openFile.title('')
        
        # Procura os JSONs de Moves0, Moves1, Moves2 e Moves3
        Moves0JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        Moves1JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves1 JSON (.json)", "*.json")] )
        Moves2JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves2 JSON (.json)", "*.json")] )
        Moves3JSON = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves3 JSON (.json)", "*.json")] )
        
        # Lê os JSONs de Moves0 e Moves1
        with open(Moves0JSON, "r", encoding='utf-8') as raw:
            jsonMoves0Data = json.load(raw)
        with open(Moves1JSON, "r", encoding='utf-8') as raw:
            jsonMoves1Data = json.load(raw)
        with open(Moves2JSON, "r", encoding='utf-8') as raw:
            jsonMoves2Data = json.load(raw)
        with open(Moves3JSON, "r", encoding='utf-8') as raw:
            jsonMoves3Data = json.load(raw)
        
        # Destrói a instância do Tkinter ()
        openFile.destroy()
        
        # Inicia os clips
        dclips = '['
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves1Data[i]['name'] + '.msm", '
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json1GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 1, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 3
        i = 0
        while i < len(jsonMoves2Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves2Data[i]['name'] + '.msm", '
            try:
                json2GoldMove = jsonMoves2Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json2GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 2, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 4
        i = 0
        while i < len(jsonMoves3Data[1:-1]):
            dclips = dclips + '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonMoves3Data[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonMoves3Data[i]['duration'], True))
            dclips = dclips + ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves3Data[i]['name'] + '.msm", '
            try:
                json3GoldMove = jsonMoves3Data[i]['goldMove']
                dclips = dclips + '"GoldMove": ' + str(json3GoldMove) + ','
            except KeyError:
                dclips = dclips + '"GoldMove": 0,'
            dclips = dclips + '"CoachId": 2, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips = dclips + '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips = dclips + ',"Duration": '
            dclips = dclips + str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips = dclips + ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips = dclips + ','
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
        
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                if (json1GoldMove != "") or (json1GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves1Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 3
        i = 0
        while i < len(jsonMoves2Data[1:-1]):
            try:
                json2GoldMove = jsonMoves2Data[i]['goldMove']
                if (json2GoldMove != "") or (json2GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves2Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 4
        i = 0
        while i < len(jsonMoves3Data[1:-1]):
            try:
                json3GoldMove = jsonMoves3Data[i]['goldMove']
                if (json3GoldMove != "") or (json3GoldMove != 0):
                    dclips = dclips + '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips = dclips + str(ubiArtTime(jsonMoves3Data[i]['time'], True))
                    dclips = dclips + ',"Duration": '
                    dclips = dclips + str(ubiArtTime(jsonMoves3Data[i]['duration'], True) + 8)
                    dclips = dclips + ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
    
    dclips = dclips + ']'
    dclips = dclips.replace(",]","]")
    arq.write(dclips)
        
    # Escreve o footer do DTAPE
    arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
    
    # Fecha o arquivo
    arq.close()
    
    # Pergunta se você quer retornar ao menu principal
    goToMain()

# Gera uma musictrack através de um JSON (funciona com todos os tipos)
def MusictrackJ2D():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a musictrack, caso seja um JSON do Just Dance Now)
    mainjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
    
    # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Lê os campos necessários do JSON para geração da musictrack
    jsonMapName = jsonMainData['MapName']
    jsonBeatData = jsonMainData['beats']
    
    # Pergunta se é um JSON do Vitality School
    QVSJSON = input(str("É um JSON do Vitality School? (Y ou N): "))
    if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja...
        # Inicializa o Tkinter novamente (para usar o seletor de arquivos)
        openFile = Tk()
        openFile.title('')
        
        # Procura o JSON de prévias do Vitality School (apenas ele é usado para gerar a musictrack)
        songprevjson = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
        
        # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
        with open(songprevjson, "r", encoding='utf-8-sig') as raw:
            jsonSPData = json.load(raw)
            
        # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
        openFile.destroy()
        
        # Lê os valores de prévia do Vitality School
        jsonStartBeatData = jsonSPData['enterTime']
        jsonLoopStartData = jsonSPData['loopStartTime']
        jsonLoopEndData = jsonSPData['loopEndTime']
        
    elif (QVSJSON == "N") or (QVSJSON == "n"): # Caso não seja, lê os valores de prévia comuns e segue com a conversão
        jsonStartBeatData = jsonMainData['AudioPreview']['coverflow']['startbeat']
        jsonLoopStartData = jsonMainData['AudioPreview']['coverflow']['startbeat']
        jsonLoopEndData = len(jsonBeatData)
    
    # Cria uma pasta com o codename da música
    createOutputDir()
    
    # Começa a escrever a musictrack (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
    arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_musictrack.tpl.ckd", "w", encoding='utf-8')
    
    # Escreve o header do musictrack
    arq.write('{"__class": "Actor_Template","WIP": 0,"LOWUPDATE": 0,"UPDATE_LAYER": 0,"PROCEDURAL": 0,"STARTPAUSED": 0,"FORCEISENVIRONMENT": 0,"COMPONENTS": [{"__class": "MusicTrackComponent_Template", "trackData": { "__class": "MusicTrackData", "structure": { "__class": "MusicTrackStructure", "markers": ')
    
    # Escreve um array para colocar as beats emendadas
    BeatsMap24 = []
    
    # Escreve as beats no formato UbiArt
    genNewBeats = input(str("Você quer gerar beats novas? (Y or N): ")) # Pergunta se novas beats devem ser geradas
    if (genNewBeats == "y") or (genNewBeats == "Y"): # Caso sim...
        NewBeats = [] # Cria um array para as beats novas
        bpm = float(input("Insira o BPM da música: ")) # Pede o BPM da música
        beat = int(round(60000/bpm))
        gerados = 0
        quantidade = len(jsonBeatData)
        while (gerados <= quantidade): # Gera os beats novos
            if gerados == quantidade:
                gerados = gerados +1
                NewBeats.append(beat*gerados)
            else:
                gerados = gerados +1
                NewBeats.append(beat*gerados)
        
        # Emenda as beats
        if (len(NewBeats) > 5 and NewBeats[0] != 0):
            NewBeats.insert(0, 0)
            firstBeat = NewBeats[0]
            nextBeats = NewBeats[0:5]
            i = 0
            while (i < 5):
                try:
                    NewBeats[i:nextBeats[i] - firstBeat]
                finally:
                    i+=1
        
        # Coloca as beats emendadas no BeatsMap24
        i = 0
        while (i < len(NewBeats)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1

        # Multiplica as beats por 48
        def multiplyBeats(number):
            return number * 48
        multipliedBeats48 = map(multiplyBeats, NewBeats)
        arrMultipliedBeats48 = list(multipliedBeats48)
        arq.write(str(arrMultipliedBeats48)) # Insere as beats multiplicadas em uma variável
        
        # Se for um valor do Vitality School...
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja, divide os valores por 48, fazendo o processo reverso para ficarem legíveis ao jogo
            jsonStartBeatData = int(int(numpy.interp(int(jsonSPData['enterTime']), NewBeats, BeatsMap24, 0)) / 48 - 24)
            jsonLoopStartData = int(int(numpy.interp(int(jsonSPData['loopStartTime']), NewBeats, BeatsMap24, 0)) / 48 - 24)
            jsonLoopEndData = int(int(numpy.interp(int(jsonSPData['loopEndTime']), NewBeats, BeatsMap24, 0)) / 48 - 24)
                
    elif (genNewBeats == "n") or (genNewBeats == "N"): # Caso não...
        # Coloca as beats emendadas no BeatsMap24
        i = 0
        while (i < len(jsonBeatData)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1
        
        # Multiplica as beats por 48
        def multiplyBeats(number):
            return number * 48
        multipliedBeats48 = map(multiplyBeats, jsonBeatData)
        arrMultipliedBeats48 = list(multipliedBeats48)
        arq.write(str(arrMultipliedBeats48)) # Insere as beats multiplicadas em uma variável
        
        # Se for um valor do Vitality School...
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja, divide os valores por 48, fazendo o processo reverso para ficarem legíveis ao jogo
            jsonStartBeatData = int(int(numpy.interp(int(jsonSPData['enterTime']), jsonBeatData, BeatsMap24, 0)) / 48 - 24)
            jsonLoopStartData = int(int(numpy.interp(int(jsonSPData['loopStartTime']), jsonBeatData, BeatsMap24, 0)) / 48 - 24)
            jsonLoopEndData = int(int(numpy.interp(int(jsonSPData['loopEndTime']), jsonBeatData, BeatsMap24, 0)) / 48 - 24) 
    
    # Escreve o resto e o footer da musictrack
    arq.write(',"signatures":[{"__class":"MusicSignature","marker":1,"beats":3},{"__class":"MusicSignature","marker":4,"beats":4},{"__class":"MusicSignature","marker":194,"beats":3},{"__class":"MusicSignature","marker":197,"beats":4}],"sections":[{"__class":"MusicSection","marker":1,"sectionType":6,"comment":""},{"__class":"MusicSection","marker":19,"sectionType":1,"comment":""},{"__class":"MusicSection","marker":52,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":68,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":84,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":100,"sectionType":1,"comment":""},{"__class":"MusicSection","marker":132,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":148,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":164,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":190,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":196,"sectionType":2,"comment":""},{"__class":"MusicSection","marker":194,"sectionType":6,"comment":""},{"__class":"MusicSection","marker":259,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":195,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":291,"sectionType":7,"comment":""}], "startBeat": 0, "endBeat": ' + str(len(jsonBeatData)) + ', "videoStartTime": 0, "previewEntry": ' + str(jsonStartBeatData) + ', "previewLoopStart": ' + str(jsonLoopStartData) + ', "previewLoopEnd": ' + str(jsonLoopEndData) + ', "volume": 0}, "path": "world/maps/' + jsonMapName.lower() + '/audio/' + jsonMapName.lower() + '.wav", "url": "jmcs://jd-contents/' + jsonMapName + '/' + jsonMapName + '.ogg"}}]}')
    
    # Fecha o arquivo
    arq.close()
    
    # Pergunta se você quer retornar ao menu principal
    goToMain()
 
# Corta pictos-atlas e os converte para TGA.CKD
def PictosAtlasJ2D():
    # Código original por mishok, adaptado levemente para uso em conjunto com a ferramenta por WodsonKun
    # Inicializa o Tkinter novamente (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura os arquivos necessários para cortar o pictos-atlas
    picatls_png = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione sua imagem pictos-atlas", filetypes=[("Pictos-Atlas (.png)", "*.png")] )
    picatls_json = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON pictos-atlas", filetypes=[("JSON Pictos-Atlas (.json)", "*.json")] )
    
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Lê o codename do JSON principal
    jsonMapName = input(str("Digite o codename da música: "))
    
    # Criar uma pasta para armazenar os pictos
    try:
        os.makedirs('output/' + jsonMapName + '/pictos')
        os.makedirs('tmp_output/pictos_png')
        os.makedirs('tmp_output/pictos_dds')
    except:
        pass
    
    # Abre o JSON e o PNG do pictos-atlas
    with open(picatls_json) as raw:
        jsonData = json.load(raw)
    fp = open(picatls_png,"rb")
    pngLoad = Image.open(fp)
    
    # Informações dos pictos-atlas
    totalPictos = len(jsonData['images'])
    pictosList = list(jsonData['images'])
    widthSize = jsonData['imageSize']['width']
    heigthSize = jsonData['imageSize']['height']

    running = True
    cP = 0
    while running:
        if cP < totalPictos:
            cXY = jsonData['images'][pictosList[cP]]
            left = cXY[0]
            top = cXY[1]
            right = cXY[0] + widthSize
            bottom = cXY[1] + heigthSize
            cropped_example = pngLoad.crop((left, top, right, bottom))
            cropped_example.save('tmp_output/pictos_png/' + pictosList[cP] + ".png")
        else:
            running = False

        cP += 1
        pass
    
    # Converte os pictogramas de PNG para DDS
    for pictopng in os.listdir('tmp_output/pictos_png/'):
        os.system('bin\\nvcompress -bc3 -silent "tmp_output\\pictos_png\\' + pictopng + '" "tmp_output\\pictos_dds\\' + pictopng.replace(".png", ".dds"))
        
    # Converte os pictogramas de DDS para TGA.CKD
    for pictodds in os.listdir('tmp_output/pictos_dds/'):
        subprocess.check_call('bin\\quickbms -Q -o "bin\\scriptDDStoCKD.bms" "tmp_output\\pictos_dds\\' + pictodds + '" "output\\' + jsonMapName + '\\pictos' ,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Limpa a pasta temporária
    shutil.rmtree("tmp_output")
    
    # Pergunta se você quer retornar ao menu principal
    goToMain()

# Corta pictos-sprite e os converte para TGA.CKD
def PictosSpriteJ2D():
    # Código original por icebb, adaptado levemente para uso em conjunto com a ferramenta por WodsonKun
    # Inicializa o Tkinter novamente (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura os arquivos necessários para cortar o pictos-sprite
    picsprt_png = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione sua imagem pictos-sprite", filetypes=[("Pictos-Sprite (.png)", "*.png")] )
    picsprt_css = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu CSS pictos-sprite", filetypes=[("CSS Pictos-Sprite (.css)", "*.css")] )
    
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Lê o codename do JSON principal
    jsonMapName = input(str("Digite o codename da música: "))
    
    # Criar uma pasta para armazenar os pictos
    try:
        os.makedirs('output/' + jsonMapName + '/pictos')
        os.makedirs('tmp_output/pictos_png')
        os.makedirs('tmp_output/pictos_dds')
    except:
        pass
    
    # Abre o PNG do pictos-sprite
    picsprt_img = Image.open(picsprt_png)
    
    # Informações dos pictos a serem cortados
    manypictos = picsprt_img.size[0] / 256
    width, height = picsprt_img.size
    
    # Valores padrão
    left = 0
    top = height - 256
    right = 256
    bottom = 2 * height - 256
    
    # Abre o CSS e corta os pictos
    i = 0
    for line in open(picsprt_css):
        while ((line[(i - 1):i]) == "{") == False:
            i += 1
        if ((line[(i - 1):i]) == "{") == True:
            i -= 1
            picto = (line[7:i])
            i = 0
            cropped_picto = picsprt_img.crop((left, top, right, bottom))
            cropped_picto.save('tmp_output/pictos_png/' + picto + '.png')
            left += 256
            right += 256
    
    # Converte os pictogramas de PNG para DDS
    for pictopng in os.listdir('tmp_output/pictos_png/'):
        os.system('bin\\nvcompress -bc3 -silent "tmp_output\\pictos_png\\' + pictopng + '" "tmp_output\\pictos_dds\\' + pictopng.replace(".png", ".dds"))
        
    # Converte os pictogramas de DDS para TGA.CKD
    for pictodds in os.listdir('tmp_output/pictos_dds/'):
        subprocess.check_call('bin\\quickbms -Q -o "bin\\scriptDDStoCKD.bms" "tmp_output\\pictos_dds\\' + pictodds + '" "output\\' + jsonMapName + '\\pictos' ,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Limpa a pasta temporária
    shutil.rmtree("tmp_output")

if __name__=='__main__':
    while(True):
        os.system('cls')
        print("E aí? Bem vindo ao JSON2DTAPE do WodsonKun!")
        print("Créditos a: planedec50, augustodoidin")
        print("Selecione uma opção:")
        print("-----------------------------")
        print("[1] Gere uma songdesc através de um JSON")
        print("[2] Gere um KTAPE através de um JSON")
        print("[3] Gere um DTAPE através de um JSON")
        print("[4] Gere um Musictrack através de um JSON")
        print("[5] Cortar pictos-atlas (Now (novo) / Vitality School)")
        print("[6] Cortar pictos-sprite (Now (velho))")
        print("[7] Sair do JSON2DTAPE")
        print("-----------------------------")
        
        option = ''
        try:
            option = int(input('Escolha sua opção: '))
        except:
            print('Opção inválida! Por favor, escolha uma opção válida')
        #Check what choice was entered and act accordingly
        if option == 1:
            SongDescJ2D()
        if option == 2:
            KTAPEJ2D()
        if option == 3:
            DTAPEJ2D()
        if option == 4:
            MusictrackJ2D()
        if option == 5:
            PictosAtlasJ2D()
        if option == 6:
            PictosSpriteJ2D()
        if option == 7:
            print('Obrigado por usar nosso JSON2DTAPE!')
            time.sleep(2)
            exit()
        else:
            print('Opção inválida! Por favor, escolha uma opção válida')