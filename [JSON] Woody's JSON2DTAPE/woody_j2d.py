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

########################################################################## WodsonKun's JSON2DTAPE (v1.2.0) #########################################################################
######################################################################## Créditos a planedec50, augustodoidin ######################################################################

### Cria um songdesc através de um JSON (funciona com todos os tipos)
def SongDescJ2D(mainjson):
    # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
    
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
    os.makedirs("output//" + jsonMapName, exist_ok=True) # Cria uma pasta com o codename da música do JSON
    
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
    elif (jsonNumCoach == "Quartet" or jsonNumCoach == 4 or jsonNumCoach == "Quatuor"):
        arq.write('"coach1": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_3_phone.png", "coach4": "world/maps/' + jsonMapName.lower() + '/menuart/textures/' + jsonMapName.lower() + '_coach_4_phone.png"')
    arq.write('},')
    if (jsonNumCoach == "Solo" or jsonNumCoach == 1):
        arq.write('"NumCoach": ' + str(1) + ',')
    elif (jsonNumCoach == "Duo" or jsonNumCoach == 2):
        arq.write('"NumCoach": ' + str(2) + ',')
    elif (jsonNumCoach == "Trio" or jsonNumCoach == 3):
        arq.write('"NumCoach": ' + str(3) + ',')
    elif (jsonNumCoach == "Quartet" or jsonNumCoach == 4 or jsonNumCoach == "Quatuor"):
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
def KTAPEJ2D(mainjson):
    # Pergunta se é um JSON do Vitality School
    QVSJSON = input(str("É um JSON do Vitality School? (Y ou N): "))
    if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja...
        QPinYin = input(str("Deseja converter o KTAPE para PinYin? (Isso os torna legíveis para a Old Gen): "))
    
    # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
    
    # Lê os campos necessários para gerar o KTAPE
    jsonMapName = jsonMainData['MapName']
    jsonBeatData = jsonMainData['beats']
    jsonLyricData = jsonMainData['lyrics']
    
    # Cria a pasta com o codenome da música
    os.makedirs("output//" + jsonMapName, exist_ok=True) # Cria uma pasta com o codename da música do JSON
    
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
                
    elif (genNewBeats == "n") or (genNewBeats == "N"):
        # Faz o cálculo necessário para as beats
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja um JSON do Vitality School...
            NewBeats = [] # Cria um array para as beats novas, já que converter as normais direto do JSON resulta em valores absurdos
            bpminit = jsonBeatData[30] - jsonBeatData[29] # Faz o cálculo inicial do BPM, diminuindo o valor de uma beat por outra (Nota: isso não dá o BPM exato, pois há chance da música ter Tempo Change)
            bpm = float(60000 / bpminit) # Faz o cálculo do BPM, dividindo 60000 pelo valor, dando o BPM (como float, para ser mais exato)
            beat = int(round(60000/bpm)) # Faz o valor final, dividindo 60000 pelo valor do BPM, iniciando a sequência de beats
            gerados = 0
            quantidade = len(jsonBeatData)
            while (gerados <= quantidade): # Gera os beats novos
                if gerados == quantidade:
                    gerados = gerados +1
                    NewBeats.append(beat*gerados)
                else:
                    gerados = gerados +1
                    NewBeats.append(beat*gerados)
            
            # Re-arranges beats from NewBeats to jsonBeatData
            jsonBeatData = []
            jsonBeatData = NewBeats
        
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
        
        elif (QVSJSON == "N") or (QVSJSON == "n"): # Caso seja um JSON do Vitality School...
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

    # ubiArtTime (por: planedec50, WodsonKun)
    def ubiArtTime(jsonTimeValue, parse):
        if (genNewBeats == "y") or (genNewBeats == "Y"): # Se novas beats tenham sido geradas...
            if bool(parse):
                return int(numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0)) # Caso seja "verdadeiro", ele faz a interpolação dos valores e retorna os mesmos
            elif not bool(parse):
                return numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0) 
        if (genNewBeats == "n") or (genNewBeats == "N"):
            if (QVSJSON == "Y") or (QVSJSON == "y"):
                if bool(parse):
                    return int(numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0)) # Caso seja "verdadeiro", ele faz a interpolação dos valores e retorna os mesmos
                elif not bool(parse):
                    return numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0) 
            else:
                if bool(parse):
                    return int(numpy.interp(jsonTimeValue, jsonBeatData, BeatsMap24, 0))
                elif not bool(parse):
                    return numpy.interp(jsonTimeValue, jsonBeatData, BeatsMap24, 0)
    
    # Começa a escrever o KTAPE (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
    arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_tml_karaoke.ktape.ckd", "w", encoding='utf-8')
    
    # Escreve o header do KTAPE
    arq.write('{"__class": "Tape","Clips": ')
    
    # Escreve os clips do KTAPE
    i = 0
    clips = '['
    while i < len(jsonMainData['lyrics'][1:-1]):
        clips += '{"__class": "KaraokeClip","Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
        clips += str(ubiArtTime(jsonLyricData[i]['time'], True))
        clips += ',"Duration": '
        clips += str(ubiArtTime(jsonLyricData[i]['duration'], True))
        if (QVSJSON == "Y") or (QVSJSON == "y"):
            if (QPinYin == "Y") or (QPinYin == "y"):
                if (jsonLyricData[i - 1]['isLineEnding'] == 1): 
                    clips += ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[i]['text'])).capitalize() + ' ","IsEndOfLine": '
                elif (jsonLyricData[i]['isLineEnding'] == 1): 
                    clips += ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[i]['text'])) + '","IsEndOfLine": '
                else:
                    clips += ',"Pitch": 8.661958,"Lyrics": "' + unidecode.unidecode(pinyin_jyutping_sentence.pinyin(jsonLyricData[i]['text'])) + ' ","IsEndOfLine": '
            if (QPinYin == "N") or (QPinYin == "n"):
                clips += ',"Pitch": 8.661958,"Lyrics": "' + jsonLyricData[i]['text'] + '","IsEndOfLine": '
        else:
            clips += ',"Pitch": 8.661958,"Lyrics": "' + jsonLyricData[i]['text'] + '","IsEndOfLine": '
        try:
            clips += str(jsonLyricData[i]['isLineEnding'])
        except KeyError:
            clips += '0'
        clips += ',"ContentType": 0,"StartTimeTolerance": 4,"EndTimeTolerance": 4,"SemitoneTolerance": 5}'
        clips += ','
        i += 1
    clips += ']'
    clips = clips.replace(",]","]")
    arq.write(clips)
    
    # Escreve o footer do KTAPE
    arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
    
    # Fecha o arquivo
    arq.close()

# Gera um DTAPE através do JSON principal e dos JSONs de moves
def DTAPEJ2D(mainjson):
    # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
    
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
    os.makedirs("output//" + jsonMapName, exist_ok=True) # Cria uma pasta com o codename da música do JSON
    
    # Pergunta se é um JSON do Vitality School
    QVSJSON = input(str("É um JSON do Vitality School? (Y ou N): "))
    
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
                
    elif (genNewBeats == "n") or (genNewBeats == "N"):
        # Faz o cálculo necessário para as beats
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja um JSON do Vitality School...
            NewBeats = [] # Cria um array para as beats novas, já que converter as normais direto do JSON resulta em valores absurdos
            bpminit = jsonBeatData[30] - jsonBeatData[29] # Faz o cálculo inicial do BPM, diminuindo o valor de uma beat por outra (Nota: isso não dá o BPM exato, pois há chance da música ter Tempo Change)
            bpm = float(60000 / bpminit) # Faz o cálculo do BPM, dividindo 60000 pelo valor, dando o BPM (como float, para ser mais exato)
            beat = int(round(60000/bpm)) # Faz o valor final, dividindo 60000 pelo valor do BPM, iniciando a sequência de beats
            gerados = 0
            quantidade = len(jsonBeatData)
            while (gerados <= quantidade): # Gera os beats novos
                if gerados == quantidade:
                    gerados = gerados +1
                    NewBeats.append(beat*gerados)
                else:
                    gerados = gerados +1
                    NewBeats.append(beat*gerados)
            
            # Re-arranges beats from NewBeats to jsonBeatData
            jsonBeatData = []
            jsonBeatData = NewBeats
        
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
        
        elif (QVSJSON == "N") or (QVSJSON == "n"): # Caso seja um JSON do Vitality School...
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

    # ubiArtTime (por: planedec50, WodsonKun)
    def ubiArtTime(jsonTimeValue, parse):
        if (genNewBeats == "y") or (genNewBeats == "Y"): # Se novas beats tenham sido geradas...
            if bool(parse):
                return int(numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0)) # Caso seja "verdadeiro", ele faz a interpolação dos valores e retorna os mesmos
            elif not bool(parse):
                return numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0) 
        if (genNewBeats == "n") or (genNewBeats == "N"):
            if (QVSJSON == "Y") or (QVSJSON == "y"):
                if bool(parse):
                    return int(numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0)) # Caso seja "verdadeiro", ele faz a interpolação dos valores e retorna os mesmos
                elif not bool(parse):
                    return numpy.interp(jsonTimeValue, NewBeats, BeatsMap24, 0) 
            else:
                if bool(parse):
                    return int(numpy.interp(jsonTimeValue, jsonBeatData, BeatsMap24, 0))
                elif not bool(parse):
                    return numpy.interp(jsonTimeValue, jsonBeatData, BeatsMap24, 0)
    
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
        Moves0JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        
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
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips += '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips += str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips += ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips += ','
            
            # Aumenta o valor de "i"
            i += 1
        
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
        Moves0JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        Moves1JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves1 JSON (.json)", "*.json")] )
        
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
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves1Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves1Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves1Data[i]['name'] + '.msm", '
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json1GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 1, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips += '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips += str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips += ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips += ','
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves1Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves1Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
        Moves0JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        Moves1JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves1 JSON (.json)", "*.json")] )
        Moves2JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves2 JSON (.json)", "*.json")] )
        
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
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves1Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves1Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves1Data[i]['name'] + '.msm", '
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json1GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 1, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 3
        i = 0
        while i < len(jsonMoves2Data[1:-1]):
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves2Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves2Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves2Data[i]['name'] + '.msm", '
            try:
                json2GoldMove = jsonMoves2Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json2GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 2, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips += '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips += str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips += ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips += ','
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves1Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves1Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves2Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves2Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
    
    # Checa quantos coaches a música tem, e caso tenha quatro coaches, procura por seus moves e os converte
    if (jsonNumCoach == "Quartet" or jsonNumCoach == 4 or jsonNumCoach == "Quatuor"):
    
        # Inicializa o Tkinter (para pegar os JSONs usando o seletor de arquivos)
        openFile = Tk()
        openFile.title('')
        
        # Procura os JSONs de Moves0, Moves1, Moves2 e Moves3
        Moves0JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves0 JSON (.json)", "*.json")] )
        Moves1JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves1 JSON (.json)", "*.json")] )
        Moves2JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves2 JSON (.json)", "*.json")] )
        Moves3JSON = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Moves3 JSON (.json)", "*.json")] )
        
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
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves0Data[i]['name'] + '.msm", '
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json0GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 0, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 2
        i = 0
        while i < len(jsonMoves1Data[1:-1]):
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves1Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves1Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves1Data[i]['name'] + '.msm", '
            try:
                json1GoldMove = jsonMoves1Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json1GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 1, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
        
        # Faz um loop para escrever a estrutura de clips dos moves do Player 3
        i = 0
        while i < len(jsonMoves2Data[1:-1]):
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves2Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves2Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves2Data[i]['name'] + '.msm", '
            try:
                json2GoldMove = jsonMoves2Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json2GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 2, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
            
        # Faz um loop para escrever a estrutura de clips dos moves do Player 4
        i = 0
        while i < len(jsonMoves3Data[1:-1]):
            dclips += '{"__class": "MotionClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": ' + str(1) + ',"StartTime": '
            dclips += str(ubiArtTime(jsonMoves3Data[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonMoves3Data[i]['duration'], True))
            dclips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMoves3Data[i]['name'] + '.msm", '
            try:
                json3GoldMove = jsonMoves3Data[i]['goldMove']
                dclips += '"GoldMove": ' + str(json3GoldMove) + ','
            except KeyError:
                dclips += '"GoldMove": 0,'
            dclips += '"CoachId": 3, "MoveType": 0, "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'
            
            # Aumenta o valor de "i"
            i += 1
    
        # Roda outro loop para escrever a estrutura de clips dos pictogramas
        i = 0
        while i < len(jsonMainData['pictos'][1:-1]):
            dclips += '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            dclips += str(ubiArtTime(jsonPictoData[i]['time'], True))
            dclips += ',"Duration": '
            dclips += str(ubiArtTime(jsonPictoData[i]['duration'], True))
            dclips += ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonPictoData[i]['name'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            dclips += ','
            
            # Aumenta o valor de "i"
            i += 1
            
        # Roda mais um loop para escrever a estrutura de clips de GoldEffect do Player 1
        i = 0
        while i < len(jsonMoves0Data[1:-1]):
            try:
                json0GoldMove = jsonMoves0Data[i]['goldMove']
                if (json0GoldMove != "") or (json0GoldMove != 0):
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves0Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves1Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves1Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves2Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves2Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
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
                    dclips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
                    dclips += str(ubiArtTime(jsonMoves3Data[i]['time'], True))
                    dclips += ',"Duration": '
                    dclips += str(ubiArtTime(jsonMoves3Data[i]['duration'], True) + 12)
                    dclips += ',"EffectType": 1},'
            except:
                pass
            
            # Aumenta o valor de "i"
            i += 1
        
    dclips += ']'
    dclips = dclips.replace(",]","]")
    arq.write(dclips)
        
    # Escreve o footer do DTAPE
    arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
    
    # Fecha o arquivo
    arq.close()

# Gera uma musictrack através de um JSON (funciona com todos os tipos)
def MusictrackJ2D(mainjson):
    # Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
    with open(mainjson, "r", encoding='utf-8-sig') as raw:
        jsonMainData = json.load(raw)
    
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
        songprevjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu SongPreviewBeats JSON", filetypes=[("SongPreviewBeats JSON (.json)", "*_SongPreviewBeats.json")] )
        
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
    os.makedirs("output//" + jsonMapName, exist_ok=True) # Cria uma pasta com o codename da música do JSON
    
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
            arrMultipliedBeats48 = list(map(multiplyBeats, NewBeats))
            arq.write(str(arrMultipliedBeats48)) # Insere as beats multiplicadas em uma variável
        arq.write(str(arrMultipliedBeats48)) # Insere as beats multiplicadas em uma variável
        
        # Se for um valor do Vitality School...
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja, divide os valores por 48, fazendo o processo reverso para ficarem legíveis ao jogo
            jsonStartBeatData = int(int(numpy.interp(int(jsonSPData['enterTime']), NewBeats, BeatsMap24, 0)) / 48)
            jsonLoopStartData = int(int(numpy.interp(int(jsonSPData['loopStartTime']), NewBeats, BeatsMap24, 0)) / 48)
            jsonLoopEndData = int(int(numpy.interp(int(jsonSPData['loopEndTime']), NewBeats, BeatsMap24, 0)) / 48)
                
    elif (genNewBeats == "n") or (genNewBeats == "N"): # Caso não...
        # Coloca as beats emendadas no BeatsMap24
        i = 0
        while (i < len(jsonBeatData)):
            try:
                BeatsMap24.append(i * 24)
            finally:
                i+=1
        
        # Faz o cálculo necessário para as beats
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja um JSON do Vitality School...
            NewBeats = [] # Cria um array para as beats novas, já que converter as normais direto do JSON resulta em valores absurdos
            bpminit = jsonBeatData[30] - jsonBeatData[29] # Faz o cálculo inicial do BPM, diminuindo o valor de uma beat por outra (Nota: isso não dá o BPM exato, pois há chance da música ter Tempo Change)
            bpm = float(60000 / bpminit) # Faz o cálculo do BPM, dividindo 60000 pelo valor, dando o BPM (como float, para ser mais exato)
            beat = int(round(60000/bpm)) # Faz o valor final, dividindo 60000 pelo valor do BPM, iniciando a sequência de beats
            gerados = 0
            quantidade = len(jsonBeatData)
            while (gerados <= quantidade): # Gera os beats novos
                if gerados == quantidade:
                    gerados = gerados +1
                    NewBeats.append(beat*gerados)
                else:
                    gerados = gerados +1
                    NewBeats.append(beat*gerados)
            
            def multiplyBeats(number):
                return number * 48
            arrMultipliedBeats48 = list(map(multiplyBeats, NewBeats)) # Multiplica e insere as beats multiplicadas em um array
            if (arrMultipliedBeats48 != 0): # Caso a primeira beat não seja 0...
                arrMultipliedBeats48.insert(0, 0) # Insere uma beat de valor 0 no início do array
            arq.write(str(arrMultipliedBeats48))
        
        elif (QVSJSON == "N") or (QVSJSON == "n"):
            def multiplyBeats(number):
                return number * 48
            arrMultipliedBeats48 = list(map(multiplyBeats, jsonBeatData))
            arq.write(str(arrMultipliedBeats48)) # Insere as beats multiplicadas em uma variável
        
        # Se for um valor do Vitality School...
        if (QVSJSON == "Y") or (QVSJSON == "y"): # Caso seja, divide os valores por 48, fazendo o processo reverso para ficarem legíveis ao jogo
            jsonStartBeatData = int(int(numpy.interp(int(jsonSPData['enterTime']), jsonBeatData, BeatsMap24, 0)) / 48)
            jsonLoopStartData = int(int(numpy.interp(int(jsonSPData['loopStartTime']), jsonBeatData, BeatsMap24, 0)) / 48)
            jsonLoopEndData = int(int(numpy.interp(int(jsonSPData['loopEndTime']), jsonBeatData, BeatsMap24, 0)) / 48) 
    
    # Escreve o resto e o footer da musictrack
    arq.write(',"signatures":[{"__class":"MusicSignature","marker":1,"beats":3},{"__class":"MusicSignature","marker":4,"beats":4},{"__class":"MusicSignature","marker":194,"beats":3},{"__class":"MusicSignature","marker":197,"beats":4}],"sections":[{"__class":"MusicSection","marker":1,"sectionType":6,"comment":""},{"__class":"MusicSection","marker":19,"sectionType":1,"comment":""},{"__class":"MusicSection","marker":52,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":68,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":84,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":100,"sectionType":1,"comment":""},{"__class":"MusicSection","marker":132,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":148,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":164,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":190,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":196,"sectionType":2,"comment":""},{"__class":"MusicSection","marker":194,"sectionType":6,"comment":""},{"__class":"MusicSection","marker":259,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":195,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":291,"sectionType":7,"comment":""}], "startBeat": 0, "endBeat": ' + str(len(jsonBeatData)) + ', "videoStartTime": 0, "previewEntry": ' + str(jsonStartBeatData) + ', "previewLoopStart": ' + str(jsonLoopStartData) + ', "previewLoopEnd": ' + str(jsonLoopEndData) + ', "volume": 0}, "path": "world/maps/' + jsonMapName.lower() + '/audio/' + jsonMapName.lower() + '.wav", "url": "jmcs://jd-contents/' + jsonMapName + '/' + jsonMapName + '.ogg"}}]}')
    
    # Fecha o arquivo
    arq.close()
 
# Corta pictos-atlas e os converte para TGA.CKD
def PictosAtlasJ2D():
    # Código original por JDEliot, adaptado levemente para uso em conjunto com a ferramenta por WodsonKun
    # Inicializa o Tkinter novamente (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura os arquivos necessários para cortar o pictos-atlas
    picatls_png = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione sua imagem pictos-atlas", filetypes=[("Pictos-Atlas (.png)", "pictos-atlas.png")] )
    picatls_json = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON pictos-atlas", filetypes=[("JSON Pictos-Atlas (.json)", "pictos-atlas.json")] )
    
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Lê o codename do JSON principal
    jsonMapName = input(str("Digite o codename da música: "))
    
    # Criar uma pasta para armazenar os pictos
    os.makedirs('output/' + jsonMapName + '/pictos', exist_ok=True)
    os.makedirs('tmp_output/pictos_png', exist_ok=True)
    os.makedirs('tmp_output/pictos_dds', exist_ok=True)
    
    # Abre o atlas e analisa suas informações básicas
    with open(picatls_json) as f:
        jsonData = json.load(f)
    sprite = Image.open(open(picatls_png,"rb"))
    pictoWidth = jsonData["imageSize"]["width"]
    pictoHeight = jsonData["imageSize"]["height"]
    
    # Conta quantos pictos tem em cada linha
    pictosPerRow = 0
    for pictocol in jsonData["images"]:
        if (jsonData["images"][pictocol][1] == 0):
            pictosPerRow += 1
    
    # Caso o atlas seja para Duo, Trio ou Quarteto, ele usa o número de pictos por linha contado anteriormente para calcular o quanto deve ser redimensionado
    if sprite.width != pictoWidth * pictosPerRow:
        sprite = sprite.resize((pictoWidth * pictosPerRow, round(sprite.height * (pictoWidth * pictosPerRow / sprite.width))), Image.BICUBIC)
    
    # Corta e redimensiona os pictos
    for picto in jsonData["images"]:
        x1 = jsonData["images"][picto][0]
        y1 = jsonData["images"][picto][1]
        x2 = x1 + pictoWidth
        y2 = y1 + pictoHeight
        sprite.crop((x1, y1, x2, y2)).resize((256,256)).save(f"tmp_output/pictos_png/{picto}.png")
    
    # Converte os pictogramas de PNG para DDS
    for pictopng in os.listdir('tmp_output/pictos_png/'):
        os.system('bin\\nvcompress -bc3 -silent "tmp_output\\pictos_png\\' + pictopng + '" "tmp_output\\pictos_dds\\' + pictopng.replace(".png", ".dds"))
        
    # Converte os pictogramas de DDS para TGA.CKD
    for pictodds in os.listdir('tmp_output/pictos_dds/'):
        subprocess.check_call('bin\\quickbms -Q -o "bin\\scriptDDStoCKD.bms" "tmp_output\\pictos_dds\\' + pictodds + '" "output\\' + jsonMapName + '\\pictos' ,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Limpa a pasta temporária
    shutil.rmtree("tmp_output")

# Corta pictos-sprite e os converte para TGA.CKD
def PictosSpriteJ2D():
    # Código original por JDEliot, adaptado levemente para uso em conjunto com a ferramenta por WodsonKun
    # Inicializa o Tkinter novamente (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura os arquivos necessários para cortar o pictos-sprite
    picsprt_png = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione sua imagem pictos-sprite", filetypes=[("Pictos-Sprite (.png)", "pictos-sprite.png")] )
    picsprt_css = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu CSS pictos-sprite", filetypes=[("CSS Pictos-Sprite (.css)", "pictos-sprite.css")] )
    
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Lê o codename do JSON principal
    jsonMapName = str(input("Digite o codename da música: "))
    
    # Pergunta quantos coaches são
    jsonNumCoach = int(input("Digite o número de coaches: "))
    
    # Criar uma pasta para armazenar os pictos
    os.makedirs('output/' + jsonMapName + '/pictos', exist_ok=True)
    os.makedirs('tmp_output/pictos_png', exist_ok=True)
    os.makedirs('tmp_output/pictos_dds', exist_ok=True)
    
    # Abre o PNG do pictos-sprite
    picsprt_img = Image.open(picsprt_png)
    
    # Corta os pictos
    if jsonNumCoach > 1:
        y1 = 40
        x1 = 217
    else:
        y1 = 0
        x1 = 256
    x = 256
    y = 0
    for picto in open(picsprt_css):
        pictoName = picto.split("-")[1].split("{")[0]
        picto = picsprt_img.crop((y,y1,x,x1))
        y = y + 256
        x = x + 256
        if (jsonNumCoach > 1):
            picto = picto.resize((256,256))
        picto.save("tmp_output/pictos_png/" + pictoName + ".png")
    
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
        print("How're you doing?")
        print("Welcome to WodsonKun's JSON2DTAPE!")
        print("Credits to: planedec50, augustodoidin")
        print("Select a option:")
        print("-----------------------------")
        print("[1] Generate a songdesc from a JSON")
        print("[2] Generate a KTAPE from a JSON")
        print("[3] Generate a DTAPE from a JSON")
        print("[4] Generate a musictrack from a JSON")
        print("[5] Cut pictos-atlas (Now [New] / Vitality School)")
        print("[6] Cut pictos-sprite (Now [Old])")
        print("[7] Converts everything at once")
        print("[8] Exits the JSON2DTAPE")
        print("-----------------------------")
        
        option = ''
        try:
            option = int(input('Choose your option: '))
        except:
            print('')
        #Check what choice was entered and act accordingly
        if option == 1:
            # Inicializa o Tkinter (para usar o seletor de arquivos)
            openFile = Tk()
            openFile.title('')
            
            # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
            mainjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
                
            # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
            openFile.destroy()
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            SongDescJ2D(mainjson)
            
        if option == 2:
            # Inicializa o Tkinter (para usar o seletor de arquivos)
            openFile = Tk()
            openFile.title('')
            
            # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
            mainjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
                
            # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
            openFile.destroy()
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            KTAPEJ2D(mainjson)
        if option == 3:
            # Inicializa o Tkinter (para usar o seletor de arquivos)
            openFile = Tk()
            openFile.title('')
            
            # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
            mainjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
                
            # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
            openFile.destroy()
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            DTAPEJ2D(mainjson)
            
        if option == 4:
            # Inicializa o Tkinter (para usar o seletor de arquivos)
            openFile = Tk()
            openFile.title('')
            
            # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
            mainjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
                
            # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
            openFile.destroy()
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            MusictrackJ2D(mainjson)
            
        if option == 5:
            PictosAtlasJ2D()
            
        if option == 6:
            PictosSpriteJ2D()
            
        if option == 7:
            # Inicializa o Tkinter (para usar o seletor de arquivos)
            openFile = Tk()
            openFile.title('')
            
            # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
            mainjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
                
            # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
            openFile.destroy()
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            SongDescJ2D(mainjson)
            DTAPEJ2D(mainjson)
            KTAPEJ2D(mainjson)
            MusictrackJ2D(mainjson)
            QPictoType = int(input("Pictos-Atlas ou Pictos-Sprite (1 = Atlas / 2 = Sprite / 3 = None)?: "))
            if (QPictoType == 1):
                PictosAtlasJ2D()
            elif (QPictoType == 2):
                PictosSpriteJ2D()
            elif (QPictoType == 3):
                pass
        
        if option == 8:
            print('Thanks for using our JSON2DTAPE!')
            time.sleep(2)
            exit()
        
        else:
            print('Wrong option! Please, choose a valid option')