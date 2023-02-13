import os, sys, io, json, time

def LyricCreate():
    # Creates empty arrays to store data
    lyricTime = []
    lyricDuration = []
    lyricName = []
    lyricLineEnding = []
    
    # Ask for a codename
    sdMapName = str(input("Type the codename of the song: "))
    
    # Creates a folder with the codename
    os.makedirs("output//" + sdMapName, exist_ok = True)
    
    # Starts writing the JSON
    songjson = open("output//" + sdMapName + "//" + sdMapName + "_lyrics.json", "w", encoding='utf-8')
    songjson.write('{"lyrics": ')
    
    # Starts recording stuff
    print('If you wanna stop, type "0" when asking for time')
    timeCheck = 0
    valTime = int(input("Write the value for the actual lyric: "))
    while (valTime != 0):
        # Time check loop
        if (timeCheck == 1):
            print('\n')
            valTime = int(input("Write the value for the actual lyric: "))
        
        # Appends everything inside their own arrays
        if (valTime != 0):
            lyricTime.append(valTime)
            valDuration = int(input("Type the duration of the lyric: "))
            lyricDuration.append(valDuration)
            valName = str(input("Write the lyric string: "))
            lyricName.append(valName)
            lineEnding = str(input("Is it the end of the line? (Y or N): "))
            if (lineEnding == "Y" or lineEnding == "y"):
                valLineEnding = 1
            elif (lineEnding == "N" or lineEnding == "n"):
                valLineEnding = 0
            lyricLineEnding.append(valLineEnding)
        
        # Changes time check, so it asks again the time value
        timeCheck = 1
    
    else:
        clipLyrics = '['
        for numLyric in range(len(lyricTime)):
            if (lyricTime[numLyric] != 0):
                clipLyrics += '{"time": ' + str(lyricTime[numLyric]) + ','
                clipLyrics += '"duration": ' + str(lyricDuration[numLyric]) + ','
                clipLyrics += '"text": "' + lyricName[numLyric] + '",'
                clipLyrics += '"isLineEnding": ' + str(lyricLineEnding[numLyric]) + '},'
  
    clipLyrics += ']'
    clipLyrics = clipLyrics.replace(",]","]")
    songjson.write(clipLyrics)
    songjson.write('}')
    songjson.close()

def PictoCreate():
    # Creates empty arrays to store data
    pictoTime = []
    pictoName = []
    
    # Ask for a codename
    sdMapName = str(input("Type the codename of the song: "))
    
    # Creates a folder with the codename
    os.makedirs("output//" + sdMapName, exist_ok = True)
    
    # Starts writing the JSON
    songjson = open("output//" + sdMapName + "//" + sdMapName + "_pictos.json", "w", encoding='utf-8')
    songjson.write('{"pictos": ')
    
    # Starts recording stuff
    print('If you wanna stop, type "0" when asking for time')
    timeCheck = 0
    valTime = int(input("Write the value for the actual picto: "))
    while (valTime != 0):
        # Time check loop
        if (timeCheck == 1):
            print('\n')
            valTime = int(input("Write the value for the actual picto: "))
        
        # Appends everything inside their own arrays
        if (valTime != 0):
            pictoTime.append(valTime)
            valName = str(input("Write the pictogram name (leave blank for 'placeholder'): "))
            if (valName != ""):
                pictoName.append(valName)
            elif (valName == ""):
                pictoName.append("placeholder")
        
        # Changes time check, so it asks again the time value
        timeCheck = 1
    
    else:
        clipPictos = '['
        for numPicto in range(len(pictoTime)):
            if (pictoTime[numPicto] != 0):
                clipPictos += '{"time": ' + str(pictoTime[numPicto]) + ','
                clipPictos += '"duration": 24,'
                clipPictos += '"name": "' + pictoName[numPicto] + '"},'
  
    clipPictos += ']'
    clipPictos = clipPictos.replace(",]","]")
    songjson.write(clipPictos)
    songjson.write('}')
    songjson.close()
    
def MoveCreate():
    # Creates empty arrays to store data
    moveTime = []
    moveDuration = []
    moveName = []
    
    # Ask for a codename
    sdMapName = str(input("Type the codename of the song: "))
    
    # Creates a folder with the codename
    os.makedirs("output//" + sdMapName, exist_ok = True)
    
    # Starts writing the JSON
    songjson = open("output//" + sdMapName + "//" + sdMapName + "_moves.json", "w", encoding='utf-8')
    
    # Starts recording stuff
    print('If you wanna stop, type "0" when asking for time')
    timeCheck = 0
    valTime = int(input("Write the value for the actual picto: "))
    while (valTime != 0):
        # Time check loop
        if (timeCheck == 1):
            print('\n')
            valTime = int(input("Write the value for the actual picto: "))
        
        # Appends everything inside their own arrays
        if (valTime != 0):
            moveTime.append(valTime)
            valDuration = int(input("Type the duration of the move: "))
            moveDuration.append(valDuration)
            valName = str(input("Write the move name (leave blank for 'placeholder'): "))
            if (valName != ""):
                moveName.append(valName)
            elif (valName == ""):
                moveName.append("placeholder")
        
        # Changes time check, so it asks again the time value
        timeCheck = 1
    
    else:
        clipMoves = '['
        for numMove in range(len(moveTime)):
            if (moveTime[numMove] != 0):
                clipMoves += '{"time": ' + str(moveTime[numMove]) + ','
                clipMoves += '"duration": ' + str(moveDuration[numMove]) + ','
                clipMoves += '"name": "' + moveName[numMove] + '"},'
  
    clipMoves += ']'
    clipMoves = clipMoves.replace(",]","]")
    songjson.write(clipMoves)
    songjson.close()

if __name__ == '__main__':
    os.makedirs('output', exist_ok = True)  
    while(True):
        print("                                          Welcome to WodsonKun's JSONCreationTool!")
        print("Select a option:")
        print("-----------------------------")
        print("[1] Generates a JSON for lyrics")
        print("[2] Generates a JSON for pictos")
        print("[3] Generates a JSON for moves")
        print("[4] Generate beats and place them in a JSON (not working yet)")
        print("[5] Creates a template Just Dance Now JSON (not working yet)")
        print("[6] Exit the JSONCreationTool")
        print("-----------------------------")
        
        option = input('Enter your choice: ')

        #Check what choice was entered and act accordingly
        if option == "1":
            LyricCreate()
        if option == "2":
            PictoCreate()
        if option == "3":
            MoveCreate()
        if option == "4":
            exit()
        if option == "5":
            exit()
        if option == "6":
            print('Thanks for using our creation tool!')
            time.sleep(2)
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 3.')
            time.sleep(1)