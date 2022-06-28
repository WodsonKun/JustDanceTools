# Importar dependências necessárias
import os, io, sys, json, time, math, unidecode, pathlib, random, numpy, shutil, subprocess
from tkinter import *
from tkinter import filedialog

# Fix a Main JSON
def mod_main_json(mainjson, time_func, time_value, dur_func, dur_value):
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
    
    # Lê as informações de AudioPreview (resumindo, coisa que o JSON2DTAPE vai precisar pro musictrack)
    jsonPreviewData = jsonMainData['AudioPreview']
    jsonCoverflowData = jsonPreviewData['coverflow']
    jsonStartbeatValue = jsonCoverflowData['startbeat']
    jsonAudioPreviewFadeValue = jsonMainData['AudioPreviewFadeTime']
    
    # Cria a pasta com o codenome da música
    os.makedirs("output//" + jsonMapName, exist_ok=True) # Cria uma pasta com o codename da música do JSON
    
    # Começa a escrever a base do JSON
    arq = open('output//' + jsonMapName + '//' + jsonMapName + '_main.json', "w", encoding='utf-8-sig')
    arq.write('{"MapName": "' + jsonMapName + '","JDVersion": 2017,"OriginalJDVersion": 2017,"Artist": "' + jsonArtist + '","Title": "' + jsonTitle + '","Credits": "' + jsonCredits + '","NumCoach": ' + str(jsonNumCoach) + ',"CountInProgression": 1,"DancerName": "Unknown Dancer","LocaleID": 4294967295,"MojoValue": 0,"Mode": 6,"Status": 3,"LyricsType": 0,"BackgroundType": 0,"Difficulty": 2,"MojoValue": 0,"DefaultColors": {"lyrics": "0xFFFFFFFF","theme": "0xFFFFFFFF","songcolor_1A": "0xFFFFFFFF","songcolor_1B": "0xFFFFFFFF","songcolor_2A": "0xFFFFFFFF","songcolor_2B": "0xFFFFFFFF"},"lyricsColor": "#FF0000","videoOffset": ' + str(jsonVideoOffset) + ',"beats": ' + str(jsonBeatData) + ',"lyrics": ')
    
    if (QKey == "lyrics" or QKey == "both"):
        lyricClips = '['
        for lyricText in range(len(jsonLyricData)):
            if time_func == "plus":
                if dur_func == "plus":
                    lyricClips += '{'
                    lyricClips += '"time": ' + str(jsonLyricData[lyricText]['time'] + time_value) + ','
                    lyricClips += '"duration": ' + str(jsonLyricData[lyricText]['duration'] + dur_value) + ','
                    lyricClips += '"text": "' + jsonLyricData[lyricText]['text'] + '",'
                    lyricClips += '"isLineEnding": ' + str(jsonLyricData[lyricText]['isLineEnding'])
                    lyricClips += '},'
                elif dur_func == "minus":
                    lyricClips += '{'
                    lyricClips += '"time": ' + str(jsonLyricData[lyricText]['time'] + time_value) + ','
                    lyricClips += '"duration": ' + str(jsonLyricData[lyricText]['duration']- dur_value) + ','
                    lyricClips += '"text": "' + jsonLyricData[lyricText]['text'] + '",'
                    lyricClips += '"isLineEnding": ' + str(jsonLyricData[lyricText]['isLineEnding'])
                    lyricClips += '},'
            elif time_func == "minus":
                if dur_func == "plus":
                    lyricClips += '{'
                    lyricClips += '"time": ' + str(jsonLyricData[lyricText]['time'] - time_value) + ','
                    lyricClips += '"duration": ' + str(jsonLyricData[lyricText]['duration'] + dur_value) + ','
                    lyricClips += '"text": "' + jsonLyricData[lyricText]['text'] + '",'
                    lyricClips += '"isLineEnding": ' + str(jsonLyricData[lyricText]['isLineEnding'])
                    lyricClips += '},'
                elif dur_func == "minus":
                    lyricClips += '{'
                    lyricClips += '"time": ' + str(jsonLyricData[lyricText]['time'] - time_value) + ','
                    lyricClips += '"duration": ' + str(jsonLyricData[lyricText]['duration'] - dur_value) + ','
                    lyricClips += '"text": "' + jsonLyricData[lyricText]['text'] + '",'
                    lyricClips += '"isLineEnding": ' + str(jsonLyricData[lyricText]['isLineEnding'])
                    lyricClips += '},'
                        
        lyricClips += '],'
        lyricClips = lyricClips.replace(',]', ']')
        arq.write(lyricClips)
    else:
        arq.write(str(jsonLyricData).replace("'", '"'))
    
    # Writes pictos
    arq.write('"pictos": ')
    pictoClips = '['
    if (QKey == "pictos" or QKey == "both"):
        for pictoEntry in range(len(jsonPictoData)):
            if time_func == "plus":
                if dur_func == "plus":
                        pictoClips += '{'
                        pictoClips += '"time": ' + str(jsonPictoData[pictoEntry]['time'] + time_value) + ','
                        pictoClips += '"duration": ' + str(jsonPictoData[pictoEntry]['duration'] + dur_value) + ','
                        pictoClips += '"name": "' + jsonPictoData[pictoEntry]['name'] + '"'
                        pictoClips += '},'
                elif dur_func == "minus":
                        pictoClips += '{'
                        pictoClips += '"time": ' + str(jsonPictoData[pictoEntry]['time'] + time_value) + ','
                        pictoClips += '"duration": ' + str(jsonPictoData[pictoEntry]['duration'] - dur_value) + ','
                        pictoClips += '"name": "' + jsonPictoData[pictoEntry]['name'] + '"'
                        pictoClips += '},'
            elif time_func == "minus":
                if dur_func == "plus":
                        pictoClips += '{'
                        pictoClips += '"time": ' + str(jsonPictoData[pictoEntry]['time'] + time_value) + ','
                        pictoClips += '"duration": ' + str(jsonPictoData[pictoEntry]['duration'] + dur_value) + ','
                        pictoClips += '"name": "' + jsonPictoData[pictoEntry]['name'] + '"'
                        pictoClips += '},'
                elif dur_func == "minus":
                        pictoClips += '{'
                        pictoClips += '"time": ' + str(jsonPictoData[pictoEntry]['time'] + time_value) + ','
                        pictoClips += '"duration": ' + str(jsonPictoData[pictoEntry]['duration'] - dur_value) - ','
                        pictoClips += '"name": "' + jsonPictoData[pictoEntry]['name'] + '"'
                        pictoClips += '},'
        
        pictoClips += '],'
        pictoClips = pictoClips.replace(',]', ']')
        arq.write(pictoClips)
    else:
        arq.write(str(jsonPictoData).replace("'", '"'))
    
    # Writes the footer of the JSON
    arq.write(',"AudioPreview": {"coverflow": {"startbeat": ' + str(jsonStartbeatValue) + '},"prelobby": {"startbeat": ' + str(jsonStartbeatValue) + '}},"AudioPreviewFadeTime": ' + str(jsonAudioPreviewFadeValue) + '}')
    arq.close()
    
# Fix a Moves JSON
def mod_moves_json(movesjson, time_func, time_value, dur_func, dur_value):
    with open(movesjson, "r") as raw:
        jsonMovesData = json.load(raw)
    
    # Creates the new JSON file
    if ("_moves0" in movesjson):
        arq = open('output//' + os.path.basename(movesjson).replace("_moves0.json", "") + '//' + os.path.basename(movesjson), "w")
    elif ("_moves1" in movesjson):
        arq = open('output//' + os.path.basename(movesjson).replace("_moves1.json", "") + '//' + os.path.basename(movesjson), "w")
    elif ("_moves2" in movesjson):
        arq = open('output//' + os.path.basename(movesjson).replace("_moves2.json", "") + '//' + os.path.basename(movesjson), "w")
    elif ("_moves3" in movesjson):
        arq = open('output//' + os.path.basename(movesjson).replace("_moves3.json", "") + '//' + os.path.basename(movesjson), "w")
    
    # Writes the movesNum JSON
    moveClips = '['
    for moveEntry in range(len(jsonMovesData)):
        if time_func == "plus":
            if dur_func == "plus":
                moveClips += '{'
                moveClips += '"name": "' + jsonMovesData[moveEntry]['name'] + '",'
                moveClips += '"time": ' + str(jsonMovesData[moveEntry]['time'] + time_value) + ','
                try:
                    jsonGoldMove = jsonMovesData[moveEntry]['goldMove']
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] + dur_value) + ','
                    moveClips += '"goldMove": ' + str(jsonGoldMove)
                    moveClips += '},'
                except KeyError:
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] + dur_value)
                    moveClips += '},'
            elif dur_func == "minus":
                moveClips += '{'
                moveClips += '"name": "' + jsonMovesData[moveEntry]['name'] + '",'
                moveClips += '"time": ' + str(jsonMovesData[moveEntry]['time'] + time_value) + ','
                try:
                    jsonGoldMove = jsonMovesData[moveEntry]['goldMove']
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] - dur_value) + ','
                    moveClips += '"goldMove": ' + str(jsonGoldMove)
                    moveClips += '},'
                except KeyError:
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] - dur_value)
                    moveClips += '},'
        elif time_func == "minus":
            if dur_func == "plus":
                moveClips += '{'
                moveClips += '"name": "' + jsonMovesData[moveEntry]['name'] + '",'
                moveClips += '"time": ' + str(jsonMovesData[moveEntry]['time'] - time_value) + ','
                try:
                    jsonGoldMove = jsonMovesData[moveEntry]['goldMove']
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] + dur_value) + ','
                    moveClips += '"goldMove": ' + str(jsonGoldMove)
                    moveClips += '},'
                except KeyError:
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] + dur_value)
                    moveClips += '},'
            elif dur_func == "minus":
                moveClips += '{'
                moveClips += '"name": "' + jsonMovesData[moveEntry]['name'] + '",'
                moveClips += '"time": ' + str(jsonMovesData[moveEntry]['time'] - time_value) + ','
                try:
                    jsonGoldMove = jsonMovesData[moveEntry]['goldMove']
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] - dur_value) + ','
                    moveClips += '"goldMove": ' + str(jsonGoldMove)
                    moveClips += '},'
                except KeyError:
                    moveClips += '"duration": ' + str(jsonMovesData[moveEntry]['duration'] - dur_value)
                    moveClips += '},'
    
    moveClips += ']'
    moveClips = moveClips.replace(',]', ']')
    arq.write(moveClips)
    arq.close()
    
if __name__=='__main__':
    while(True):
        os.system('cls')
        print("How're you doing?")
        print("Welcome to WodsonKun's JSONFix Tool!")
        print("Select a option:")
        print("-----------------------------")
        print("[1] Fix a Main JSON")
        print("[2] Fix a Moves JSON")
        print("[3] Exits the JSONFix Tool")
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
            
            QKey = str(input('Do you wanna fix lyrics, pictos or both ("lyrics", "pictos" or "both")?: '))
            QTime = str(input('Do you wanna fix timings? ("Y" or "N"): '))
            QDur = str(input('Do you wanna fix durations? ("Y" or "N"): '))
            if (QTime == "Y" or QTime == "y"):
                QTimeOP = str(input('Do you wanna increase or decrease time? ("plus" or "minus"): '))
                QTimeVL = int(input('Set the time you wanna increase/decrease: '))
            else:
                QTimeOP = "plus"
                QTimeVL = 0
            if (QDur == "Y" or QDur == "y"):
                QDurOP = str(input('Do you wanna increase or decrease duration? ("plus" or "minus"): '))
                QDurVL = int(input('Set the duration value you wanna increase/decrease: '))
            else:
                QDurOP = "plus"
                QDurVL = 0
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            mod_main_json(mainjson, QTimeOP, QTimeVL, QDurOP, QDurVL)
            
        if option == 2:
            # Inicializa o Tkinter (para usar o seletor de arquivos)
            openFile = Tk()
            openFile.title('')
            
            # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
            mainjson = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Now / Vitality School JSON (.json)", "*.json")] )
                
            # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
            openFile.destroy()
            
            QTime = str(input('Do you wanna fix timings? ("Y" or "N"): '))
            QDur = str(input('Do you wanna fix durations? ("Y" or "N"): '))
            if (QTime == "Y" or QTime == "y"):
                QTimeOP = str(input('Do you wanna increase or decrease time? ("plus" or "minus"): '))
                QTimeVL = int(input('Set the time you wanna increase/decrease: '))
            else:
                QTimeOP = "plus"
                QTimeVL = 0
            if (QDur == "Y" or QDur == "y"):
                QDurOP = str(input('Do you wanna increase or decrease duration? ("plus" or "minus"): '))
                QDurVL = int(input('Set the duration value you wanna increase/decrease: '))
            else:
                QDurOP = "plus"
                QDurVL = 0
            
            # Do everything at once (Songdesc, DTAPE, KTAPE, Musictrack and pictos)
            mod_moves_json(mainjson, QTimeOP, QTimeVL, QDurOP, QDurVL)
        
        if option == 3:
            print('Thanks for using our JSON Fixing Tool!')
            time.sleep(2)
            exit()
        
        else:
            print('Wrong option! Please, choose a valid option')