import os, sys, io, math, time, json, random, shutil, pathlib, subprocess, requests, UnityPy
from tkinter import *
from tkinter import filedialog
from PIL import Image
from urllib.parse import urlparse

# Defines a Unity version to fallback in order to be able to extract the bundles through UnityPy (just in case it doesn't work automatically)
UnityPy.config.FALLBACK_UNITY_VERSION = "2021.3.9f1"

## Extra functions that helps convertions...
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
    return math.floor(random.randint(0, 40000) * (40000 - 10000 + 1) + 10000) # Gera um valor randômico e retorna o mesmo para ser usado como ID

# resizeCanvas
def resizeCanvas(old_image_path, new_image_path, canvas_width, canvas_height):
    """
    Resize the canvas of old_image_path.

    Store the new image in new_image_path. Center the image on the new canvas.

    Parameters
    ----------
    old_image_path : str
    new_image_path : str
    canvas_width : int
    canvas_height : int
    """
    im = Image.open(old_image_path)
    old_width, old_height = im.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height)))
    
    mode = im.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 0)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.paste(im, (x1, y1, x1 + old_width, y1 + old_height))
    newImage.save(new_image_path)

# Creates a "output" folder
os.makedirs('output', exist_ok = True)

# MapPackage ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CONV_MapPackage():
    # Loads Unity bundles...
    # Initializes Tkinter (to use the file picker)
    openFile = Tk()
    openFile.title('')

    # Searches for the bundle
    mapPackageBundle = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your MapPackage BUNDLE file", filetypes=[("Just Dance Next BUNDLE", "*")] )
    
    # Destroys the actual Tkinter instance
    openFile.destroy()
    
    # Parses the bundle
    with open(mapPackageBundle, 'rb+') as f:
    
        # Creates a "temp" folder
        os.makedirs('temp', exist_ok = True)
        
        env = UnityPy.load(mapPackageBundle)
        
        # TMLs (Timelines) ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Extracts every single "MonoBehaviour" file out of the .bundle
        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                # export
                if obj.serialized_type.nodes:
                    # save decoded data
                    tree = obj.read_typetree()
                    fp = os.path.join('temp', f"{tree['m_Name']}.json")
                    with open(fp, "wt", encoding = "utf8") as f:
                        if tree['m_Name'] != "":
                          jsonCodename = tree['m_Name']
                        json.dump(tree, f, ensure_ascii = False, indent = 4)
                else:
                    # save raw relevant data (without Unity MonoBehaviour header)
                    data = obj.read_typetree()
                    fp = os.path.join('temp', f"{data.name}.bin")
                    with open(fp, "wb") as f:
                        f.write(data.raw_data)
        
        # Starts reading the JSON
        # Creates a "output" folder
        os.makedirs('output\\' + jsonCodename, exist_ok = True)
        os.makedirs('output\\' + jsonCodename + "\\gestures\\durango", exist_ok = True)
        os.makedirs('output\\' + jsonCodename + "\\gestures\\x360", exist_ok = True)
        os.makedirs('output\\' + jsonCodename + "\\gestures\\orbis", exist_ok = True)
        
        # Opens the JSON
        with open('temp/' + jsonCodename + '.json', "r", encoding='utf-8-sig') as raw:
            jsonMainData = json.load(raw)
        with open('temp/.json', "r", encoding='utf-8-sig') as raw:
            jsonMTData = json.load(raw)
        
        # Loops through every UUID entry, and then gets the lyricColor
        jsonMapName = jsonMainData['SongDesc']['MapName']
        jsonOriginalJDVersion = jsonMainData['SongDesc']['OriginalJDVersion']
        jsonArtist = jsonMainData['SongDesc']['Artist']
        jsonTitle = jsonMainData['SongDesc']['Title']
        jsonCredits = jsonMainData['SongDesc']['Credits']
        jsonNumCoach = jsonMainData['SongDesc']['NumCoach']
        jsonDifficulty = jsonMainData['SongDesc']['Difficulty']
        jsonSweatDifficulty = jsonMainData['SongDesc']['SweatDifficulty']
        jsonLyricsColor = "#FFFFFF"
        
        # Songdesc ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Starts writing the songdesc (you NEED to use utf-8, 'cause every other breaks the game)
        arq = open("output" + "//" + jsonMapName + "//songdesc.tpl.ckd", "w", encoding='utf-8')
        arq.write('{"__class": "Actor_Template","WIP": 0,"LOWUPDATE": 0,"UPDATE_LAYER": 0,"PROCEDURAL": 0,"STARTPAUSED": 0,"FORCEISENVIRONMENT": 0,"COMPONENTS": [{"__class": "JD_SongDescTemplate","MapName": "' + jsonMapName + '","JDVersion": 2017,"OriginalJDVersion": 2023,"Artist": "' + jsonArtist + '","DancerName": "Unknown Dancer","Title": "' + jsonTitle + '","Credits": "' + jsonCredits + '","PhoneImages": {')
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
        arq.write('"Difficulty": ' + str(jsonDifficulty) + ',')
        arq.write('"Energy": ' + str(jsonSweatDifficulty) + ',')
        arq.write('"backgroundType": 0,"LyricsType": 0,"Tags": ["main"],"Status": 3,"LocaleID": 4294967295,"MojoValue": 0,"CountInProgression": 1,"DefaultColors":{"songcolor_2a": [1, 0.666667, 0.666667, 0.666667],  "lyrics": [1, ' + str(hex2RGB(jsonLyricsColor)[0]/255) + ', ' +  str(hex2RGB(jsonLyricsColor)[1]/255) + ', ' +  str(hex2RGB(jsonLyricsColor)[2]/255) + '], "theme": [1, 1, 1, 1],"songcolor_1a":  [1, 0.266667, 0.266667, 0.266667],"songcolor_2b": [1, 0.466667, 0.466667, 0.466667],"songcolor_1b": [1, 0.066667, 0.066667, 0.066667]},"Paths": {"Avatars": null,"AsyncPlayers": null}}]}')
        arq.close()

        # KTAPE ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Starts writing the KTAPE (you NEED to use utf-8, 'cause every other breaks the game)
        arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_tml_karaoke.ktape.ckd", "w", encoding='utf-8')
        
        # Escreve o header do KTAPE
        arq.write('{"__class": "Tape","Clips": ')
        
        # Escreve os clips do KTAPE
        clips = '['
        for KaraokeClips in range(len(jsonMainData['KaraokeData']['Clips'])):
            clips += '{"__class": "KaraokeClip","Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            clips += str(jsonMainData['KaraokeData']['Clips'][KaraokeClips]['KaraokeClip']['StartTime'])
            clips += ',"Duration": '
            clips += str(jsonMainData['KaraokeData']['Clips'][KaraokeClips]['KaraokeClip']['Duration'])
            clips += ',"Pitch": 8.661958,"Lyrics": "' + repr(jsonMainData['KaraokeData']['Clips'][KaraokeClips]['KaraokeClip']['Lyrics'])[1:-1].replace('\"', r'\"') + '","IsEndOfLine": '
            clips += str(jsonMainData['KaraokeData']['Clips'][KaraokeClips]['KaraokeClip']['IsEndOfLine'])
            clips += ',"ContentType": 0,"StartTimeTolerance": 4,"EndTimeTolerance": 4,"SemitoneTolerance": 5}'
            clips += ','
        clips += ']'
        clips = clips.replace(",]","]")
        arq.write(clips)
        arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
        arq.close()
        
        # DTAPE ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Starts writing the DTAPE (you NEED to use utf-8, 'cause every other breaks the game)
        arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_tml_dance.dtape.ckd", "w", encoding='utf-8')
        
        # Writes the DTAPE header
        arq.write('{"__class": "Tape","Clips": ')
        
        # Writes the DTAPE clips
        clips = '['
        for DanceClips in range(len(jsonMainData['DanceData']['MotionClips'])):
            clips += '{"__class": "MotionClip","Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            clips += str(jsonMainData['DanceData']['MotionClips'][DanceClips]['StartTime'])
            clips += ',"Duration": '
            clips += str(jsonMainData['DanceData']['MotionClips'][DanceClips]['Duration'])
            if (jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveType'] == 0):
                clips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveName'] + '.msm'
            elif (jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveType'] == 1):
                if (".gesture" in jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveName']):
                    gesturename = jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveName'].replace("\\", "/").replace('maps/' + jsonMapName + '/', '')
                    clips += ',"ClassifierPath": "world/' + jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveName'].replace("\\", "/")
                    
                    try:
                        # Generates generic gestures to each gesture found inside the DTAPE
                        shutil.copy('bin\generic_durango.gesture', "output" + "//" + jsonMapName + "//gestures//durango//" + gesturename.replace(f'maps/{jsonMapName.lower()}/timeline/moves/', ''))
                        shutil.copy('bin\generic_durango.gesture', "output" + "//" + jsonMapName + "//gestures//x360//" + gesturename.replace(f'maps/{jsonMapName.lower()}/timeline/moves/', ''))
                        shutil.copy('bin\generic_durango.gesture', "output" + "//" + jsonMapName + "//gestures//orbis//" + gesturename.replace(f'maps/{jsonMapName.lower()}/timeline/moves/', ''))
                    except:
                        pass
                else:
                    gesturename = jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveName']
                    clips += ',"ClassifierPath": "world/maps/' + jsonMapName.lower() + '/timeline/moves/' + jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveName'] + '.gesture'
                    
                    try:
                        # Generates generic gestures to each gesture found inside the DTAPE
                        shutil.copy('bin\generic_durango.gesture', "output" + "//" + jsonMapName + "//gestures//durango//" + gesturename + '.gesture')
                        shutil.copy('bin\generic_durango.gesture', "output" + "//" + jsonMapName + "//gestures//x360//" + gesturename + '.gesture')
                        shutil.copy('bin\generic_durango.gesture', "output" + "//" + jsonMapName + "//gestures//orbis//" + gesturename + '.gesture')
                    except:
                        pass
                
            clips += '","GoldMove": '
            clips += str(jsonMainData['DanceData']['MotionClips'][DanceClips]['GoldMove'])
            clips += ',"CoachId": '
            clips += str(jsonMainData['DanceData']['MotionClips'][DanceClips]['CoachId'])
            clips += ',"MoveType": '
            clips += str(jsonMainData['DanceData']['MotionClips'][DanceClips]['MoveType'])
            clips += ', "Color": [1, 0.968628, 0.164706, 0.552941], "MotionPlatformSpecifics": {"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"DURANGO": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0}}},'

        for PictoClips in range(len(jsonMainData['DanceData']['PictoClips'])):
            clips += '{"__class": "PictogramClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            clips += str(jsonMainData['DanceData']['PictoClips'][PictoClips]['StartTime'])
            clips += ',"Duration": '
            clips += str(jsonMainData['DanceData']['PictoClips'][PictoClips]['Duration'])
            clips += ',"PictoPath": "world/maps/' + jsonMapName.lower() + '/timeline/pictos/' + jsonMainData['DanceData']['PictoClips'][PictoClips]['PictoPath'] + '.tga", "MontagePath": "", "AtlIndex": 4294967295, "CoachCount": 4294967295}'
            clips += ','

        for GoldClips in range(len(jsonMainData['DanceData']['GoldEffectClips'])):
            clips += '{"__class": "GoldEffectClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            clips += str(jsonMainData['DanceData']['GoldEffectClips'][GoldClips]['StartTime'])
            clips += ',"Duration": '
            clips += str(jsonMainData['DanceData']['GoldEffectClips'][GoldClips]['Duration'])
            clips += ',"EffectType": 1},'
            
        clips += ']'
        clips = clips.replace(",]","]")
        arq.write(clips)
        arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
        arq.close()
        
        # Musictrack ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Começa a escrever a musictrack (obrigatório usar utf-8, pois qualquer outro encoding quebra o jogo)
        arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_musictrack.tpl.ckd", "w", encoding='utf-8')
        
        # Escreve o header do musictrack
        arq.write('{"__class": "Actor_Template","WIP": 0,"LOWUPDATE": 0,"UPDATE_LAYER": 0,"PROCEDURAL": 0,"STARTPAUSED": 0,"FORCEISENVIRONMENT": 0,"COMPONENTS": [{"__class": "MusicTrackComponent_Template", "trackData": { "__class": "MusicTrackData", "structure": { "__class": "MusicTrackStructure", "markers": ')
        
        # Writes markers
        markers = '['
        for markerData in range(len(jsonMTData['m_structure']['MusicTrackStructure']['markers'])):
            markers += str(jsonMTData['m_structure']['MusicTrackStructure']['markers'][markerData]['VAL']) + ','
        markers += ']'
        markers = markers.replace(",]","]")
        arq.write(markers)
        
        # Writes signatures
        arq.write(',"signatures": ')
        signatures = '['
        for signatureData in range(len(jsonMTData['m_structure']['MusicTrackStructure']['signatures'])):
            signatures += '{"__class": "MusicSignature",'
            signatures += '"beats": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['signatures'][signatureData]['MusicSignature']['beats'])) + ','
            signatures += '"marker": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['signatures'][signatureData]['MusicSignature']['marker'])) + ','
            signatures += '"comment": "' + jsonMTData['m_structure']['MusicTrackStructure']['signatures'][signatureData]['MusicSignature']['comment'] + '"'
            signatures += '},'
        signatures += ']'
        signatures = signatures.replace(",]","]")
        arq.write(signatures)
        
        # Writes sections
        arq.write(',"sections": ')
        sections = '['
        for sectionData in range(len(jsonMTData['m_structure']['MusicTrackStructure']['sections'])):
            sections += '{"__class": "MusicSection",'
            sections += '"sectionType": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['sections'][sectionData]['MusicSection']['sectionType'])) + ','
            sections += '"marker": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['sections'][sectionData]['MusicSection']['marker'])) + ','
            sections += '"comment": "' + jsonMTData['m_structure']['MusicTrackStructure']['sections'][sectionData]['MusicSection']['comment'] + '"'
            sections += '},'
        sections += ']'
        sections = sections.replace(",]","]")
        arq.write(sections)
        
        # Writes comments
        arq.write(',"comments": ')
        comments = '['
        for commentData in range(len(jsonMTData['m_structure']['MusicTrackStructure']['comments'])):
            comments += '{"__class": "Comment",'
            comments += '"marker": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['comments'][commentData]['Comment']['marker'])) + ','
            comments += '"comment": "' + jsonMTData['m_structure']['MusicTrackStructure']['comments'][commentData]['Comment']['comment'] + '",'
            comments += '"commentType": "' + jsonMTData['m_structure']['MusicTrackStructure']['comments'][commentData]['Comment']['commentType'] + '"'
            comments += '},'
        comments += ']'
        comments = comments.replace(",]","]")
        arq.write(comments + ',')
        
        # Writes the end of the musictrack
        arq.write('"startBeat": ' + str(jsonMTData['m_structure']['MusicTrackStructure']['startBeat']) + ',')
        arq.write('"endBeat": ' + str(jsonMTData['m_structure']['MusicTrackStructure']['endBeat']) + ',')
        arq.write('"videoStartTime": ' + str(jsonMTData['m_structure']['MusicTrackStructure']['videoStartTime']) + ',')
        arq.write('"previewEntry": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['previewEntry'])) + ',')
        arq.write('"previewLoopStart": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['previewLoopStart'])) + ',')
        try:
            arq.write('"previewLoopEnd": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['previewLoopStart'] + jsonMTData['m_structure']['MusicTrackStructure']['previewDuration'])) + ',')
        except:
            arq.write('"previewLoopEnd": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['previewLoopEnd'])) + ',')
        arq.write('"volume": 0}, "path": "world/maps/' + jsonMapName.lower() + '/audio/' + jsonMapName.lower() + '.wav", "url": "jmcs://jd-contents/' + jsonMapName + '/' + jsonMapName + '.ogg"}}]}')
        
        # Mainsequence ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Starts writing the mainsequence (you NEED to use utf-8, 'cause every other breaks the game)
        arq = open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_mainsequence.tape.ckd", "w", encoding='utf-8')
        
        # Writes the mainsequence header
        arq.write('{"__class": "Tape","Clips": ')
        
        # Writes the mainsequence clips
        clips = '['
        
        # Writes the intro SoundSetClip
        clips += '{"__class": "SoundSetClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['startBeat']) * int(24)) + ',"Duration": ' + str(int(jsonMTData['m_structure']['MusicTrackStructure']['startBeat']) * int(24) + 10000) + ',"SoundSetPath": "world/maps/' + jsonCodename.lower() + '/audio/amb/amb_' + jsonCodename.lower() + '_intro.tpl","SoundChannel": 0,"StartOffset": 0,"StopsOnEnd": 0,"AccountedForDuration": 0},'
        
        # Writes HideUserInterfaceClip clips
        for HideUserClips in range(len(jsonMainData['DanceData']['HideHudClips'])):
            clips += '{"__class": "HideUserInterfaceClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": '
            clips += str(jsonMainData['DanceData']['HideHudClips'][HideUserClips]['StartTime'])
            clips += ',"Duration": '
            clips += str(jsonMainData['DanceData']['HideHudClips'][HideUserClips]['Duration'])
            clips += ',"EventType": 18},'
        
        clips += ']'
        clips = clips.replace(",]","]")
        arq.write(clips)
        arq.write(',"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + jsonMapName + '","SoundwichEvent": ""}')
        arq.close()
        
        # AMB TPL ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Starts writing the mainsequence (you NEED to use utf-8, 'cause every other breaks the game)
        arq = open("output" + "//" + jsonMapName + "//amb_" + jsonMapName.lower() + "_intro.tpl.ckd", "w", encoding='utf-8')
        arq.write('{"__class": "Actor_Template","WIP": 0,"LOWUPDATE": 0,"UPDATE_LAYER": 0,"PROCEDURAL": 0,"STARTPAUSED": 0,"FORCEISENVIRONMENT": 0,"COMPONENTS": [{"__class": "SoundComponent_Template","soundList": [{"__class": "SoundDescriptor_Template","name": "amb_' + jsonMapName.lower() + '_intro","volume": 0,"category": "amb","limitCategory": "","limitMode": 0,"maxInstances": 4294967295,"files": ["world/maps/' + jsonMapName.lower() + '/audio/amb/amb_' + jsonMapName.lower() + '_intro.wav"],"serialPlayingMode": 0,"serialStoppingMode": 0,"params": {"__class": "SoundParams","loop": 0,"playMode": 1,"playModeInput": "","randomVolMin": 0,"randomVolMax": 0,"delay": 0,"randomDelay": 0,"pitch": 1,"randomPitchMin": 1,"randomPitchMax": 1,"fadeInTime": 0,"fadeOutTime": 0,"filterFrequency": 0,"filterType": 2,"transitionSampleOffset": 0},"pauseInsensitiveFlags": 0,"outDevices": 4294967295,"soundPlayAfterdestroy": 0}]}]}')
        arq.close()
        
        # MSMs (Moves) ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Extracts every single "TextAsset" file out of the .bundle
        # Note: Actually, those are .msm/.gesture files
        # Creates a "output" folder
        os.makedirs('output/' + jsonCodename + '/moves', exist_ok = True)
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                # parse the object data
                data = obj.read()
                with open('output/' + jsonCodename + '/moves/' + (data.name).lower(), "wb") as f:
                    f.write(bytes(data.script))
        
        # Textures ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Creates a "output" folder
        os.makedirs('output/' + jsonCodename + '/pictos', exist_ok = True)
        os.makedirs('temp/pictos', exist_ok = True)
        os.makedirs('temp/pictos/resized', exist_ok = True)
        
        # Extracts every single "Texture2D" out of the .bundle
        for obj in env.objects:
            if obj.type.name in ["Texture2D", "Sprite"]:
                # parse the object data
                data = obj.read()

                # create destination path
                dest = os.path.join('temp/pictos', data.name.lower())

                # make sure that the extension is correct
                # you probably only want to do so with images/textures
                dest, ext = os.path.splitext(dest)
                dest = dest + ".png"
                img = data.image
                if ("sactx" in (data.name)):
                    pass
                else:
                    img.save(dest)
        
        # Pictos (resizing) ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        for picto in os.listdir('temp/pictos/'):
            if ('.png' in picto):
                if (jsonNumCoach == 1):
                    resizeCanvas('temp/pictos/' + picto, 'output/' + jsonCodename + '/pictos/' + picto, 512, 512)
                elif (jsonNumCoach >= 2):
                    resizeCanvas('temp/pictos/' + picto, 'temp/pictos/resized/' + picto, 512, 350)
                    pictopng = Image.open('temp/pictos/resized/' + picto)
                    pictopng = pictopng.resize((1024,512))
                    pictopng.save('output/' + jsonCodename + '/pictos/' + picto)
    
        # Song audio ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        qAudio = str(input("Do you wanna crop the audio? (It also generates the AMB audio) (Y or N): "))
        
        if (qAudio == "Y" or qAudio == "y"):
            # Creates "jdu" directory inside of "output"
            os.makedirs('output/' + jsonMapName + '/audio', exist_ok=True)
            
            # Initializes Tkinter (file picker)
            openFile = Tk()
            openFile.title('')
            
            # Searches for the necessary file
            audiofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your audio file", filetypes=[("Audio (.ogg / .opus)", "*.ogg *.opus")])
            
            # Checks if the musictrack has a empty byte at the end, and if it has, creates a copy of the file without it
            with open("output" + "//" + jsonMapName + "//" + jsonMapName.lower() + "_musictrack.tpl.ckd", 'rb') as file_in:
                with open("temp/temp_musictrack.tpl.ckd", 'wb') as file_out:
                    data = file_in.read()
                    while data.endswith(b'\x00'):
                        data = data[:-1]
                    file_out.write(data)
            
            # Destroys Tkinter
            openFile.destroy()
            
            # Opens the musictrack
            with open("temp/temp_musictrack.tpl.ckd", "r", encoding='utf-8') as mt:
                musictrackData = json.load(mt)
            
            # Gets startBeat value
            startBeatVal = musictrackData['COMPONENTS'][0]['trackData']['structure']['startBeat']
            
            # Gets the marker value
            valMarker = musictrackData['COMPONENTS'][0]['trackData']['structure']['markers'][abs(startBeatVal)]
            
            # Turns it into a positive value (doesn't matter if the value is positive already or not) and divide it
            msVal = int(valMarker / 48)
            
            # Crops the audio (and the AMB, if chosen)
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + audiofile + '" -ss 0ms -t ' + str(msVal) + 'ms "output\\' + jsonMapName + '\\audio\\amb_' + jsonMapName.lower() + '_intro.ogg"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + audiofile + '" -ss ' + str(msVal) + 'ms "output\\' + jsonMapName + '\\audio\\' + jsonMapName.lower() + '.ogg"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            pass
        
    # Clean 'temp' folder
    shutil.rmtree('temp')

# TexturesLarge ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def EXT_TextureLarge(bundleFile):
    # Parses the bundle
    with open(bundleFile, 'rb+') as f:
        # Creates the necessary folders
        os.makedirs('temp', exist_ok = True)
        os.makedirs('temp/textures', exist_ok = True)
        os.makedirs('output/' + jsonCodename + '/textures', exist_ok = True)
        
        # Load the bundle
        env = UnityPy.load(bundleFile)
        
        # Extracts every single "Texture2D" out of the .bundle
        for obj in env.objects:
            if obj.type.name in ["Texture2D", "Sprite"]:
                data = obj.read()
                if ("map_bkg" in (data.name)):
                    dest = os.path.join('output/' + jsonCodename + '/textures', data.name.lower())
                else:
                    dest = os.path.join('temp/textures', data.name.lower())
                dest, ext = os.path.splitext(dest)
                dest = dest + ".png"
                img = data.image
                img.save(dest)
                
        # Re-sizing ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        for TextureLargeFile in os.listdir('temp/textures/'):
            if ('.png' in TextureLargeFile):
                if ("coach" in TextureLargeFile):
                    resizeCanvas('temp/textures/' + TextureLargeFile, 'output/' + jsonCodename + '/textures/' + TextureLargeFile, 1024, 1024)
                else:
                    pass

# TexturesPhone ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def EXT_TexturePhone(bundleFile):
    # Parses the bundle
    with open(bundleFile, 'rb+') as f:
    
        # Creates a "temp" folder
        os.makedirs('temp', exist_ok = True)
        os.makedirs('temp/phone_textures', exist_ok = True)
        os.makedirs('output/' + jsonCodename + '/phone_textures', exist_ok = True)
        
        # Load the bundle
        env = UnityPy.load(bundleFile)
        
        # Extracts every single "Texture2D" out of the .bundle
        for obj in env.objects:
            if obj.type.name in ["Texture2D", "Sprite"]:
                data = obj.read()
                dest = os.path.join('temp/phone_textures', data.name.lower())
                dest, ext = os.path.splitext(dest)
                dest = dest + ".png"
                img = data.image
                img.save(dest)
                
        # Re-sizing ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        for TexturePhoneFile in os.listdir('temp/phone_textures/'):
            if ('.png' in TexturePhoneFile):
                if ("coach" in TexturePhoneFile):
                    resizeCanvas('temp/phone_textures/' + TexturePhoneFile, 'output/' + jsonCodename + '/phone_textures/' + TexturePhoneFile, 256, 256)
                else:
                    pass

# GenericTexture ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def EXT_GenericTexture(bundleFile):
    # Parses the bundle
    with open(bundleFile, 'rb+') as f:
    
        # Creates a "temp" folder
        os.makedirs('temp', exist_ok = True)
        os.makedirs('temp/textures', exist_ok = True)
        os.makedirs('output/' + jsonCodename + '/textures', exist_ok = True)
        
        # Load the bundle
        env = UnityPy.load(bundleFile)
        
        # Extracts every single "Texture2D" out of the .bundle
        for obj in env.objects:
            if obj.type.name in ["Texture2D", "Sprite"]:
                data = obj.read()
                dest = os.path.join('output/' + jsonCodename + '/textures', data.name.lower())
                dest, ext = os.path.splitext(dest)
                dest = dest + ".png"
                img = data.image
                img.save(dest)

# Converts songs from Just Dance Plus
def Plus2UAF():
    # Creates the necessary folders
    os.makedirs('temp', exist_ok = True)
    
    # Opens the JSON
    with open('bin/PlusSongDB.json', "r", encoding='utf-8-sig') as raw:
        CatalogData = json.load(raw)
    
    # Get all UUIDs and store them in a array
    SongUUID = []
    for MapUUID in CatalogData:
        SongUUID.append(MapUUID)
    
    # Loops through every UUID entry, and then gets the lyricColor
    for MapNumber in range(len(SongUUID)):
        if (jsonCodename == CatalogData[SongUUID[MapNumber]]['mapName']):
            # Retrieve some info from the SongDB in order to fill the songdesc
            jsonLyricsColor = CatalogData[SongUUID[MapNumber]]['lyricsColor']
            jsonMapName = CatalogData[SongUUID[MapNumber]]['mapName']
            jsonOriginalJDVersion = CatalogData[SongUUID[MapNumber]]['originalJDVersion']
            jsonArtist = CatalogData[SongUUID[MapNumber]]['artist']
            jsonTitle = CatalogData[SongUUID[MapNumber]]['title']
            jsonCredits = CatalogData[SongUUID[MapNumber]]['credits']
            jsonNumCoach = CatalogData[SongUUID[MapNumber]]['coachCount']
            jsonDifficulty = CatalogData[SongUUID[MapNumber]]['difficulty']
            jsonSweatDifficulty = CatalogData[SongUUID[MapNumber]]['sweatDifficulty']
            
            # Also retrieves some file info in order to download them
            songCoachesLarge = CatalogData[SongUUID[MapNumber]]['assets']['coachesLarge']
            songCoachesSmall = CatalogData[SongUUID[MapNumber]]['assets']['coachesSmall']
            songCover = CatalogData[SongUUID[MapNumber]]['assets']['cover']
            songCover1024 = CatalogData[SongUUID[MapNumber]]['assets']['cover1024']
            songCoverSmall = CatalogData[SongUUID[MapNumber]]['assets']['coverSmall']
            try:
                songLogo = CatalogData[SongUUID[MapNumber]]['assets']['songTitleLogo']
            except:
                songLogo = "naur"
    
    # Downloads stuff
    r = requests.get(songCoachesLarge)
    with open('temp/' + urlparse(songCoachesLarge).path.split('/')[-1], 'wb') as f:
        f.write(r.content)
    r = requests.get(songCoachesSmall)
    with open('temp/' + urlparse(songCoachesSmall).path.split('/')[-1], 'wb') as f:
        f.write(r.content)
    r = requests.get(songCover)
    with open('temp/' + urlparse(songCover).path.split('/')[-1], 'wb') as f:
        f.write(r.content)
    r = requests.get(songCover1024)
    with open('temp/' + urlparse(songCover1024).path.split('/')[-1], 'wb') as f:
        f.write(r.content)
    r = requests.get(songCoverSmall)
    with open('temp/' + urlparse(songCoverSmall).path.split('/')[-1], 'wb') as f:
        f.write(r.content)
    if songLogo != "naur":
        r = requests.get(songLogo)
        with open('temp/' + urlparse(songLogo).path.split('/')[-1], 'wb') as f:
            f.write(r.content)
    else:
        pass
    
    # Extracts stuff
    EXT_TextureLarge('temp/' + urlparse(songCoachesLarge).path.split('/')[-1])
    EXT_TexturePhone('temp/' + urlparse(songCoachesSmall).path.split('/')[-1])
    EXT_GenericTexture('temp/' + urlparse(songCover).path.split('/')[-1])
    EXT_GenericTexture('temp/' + urlparse(songCover1024).path.split('/')[-1])
    EXT_GenericTexture('temp/' + urlparse(songCoverSmall).path.split('/')[-1])
    if songLogo != "naur":
        EXT_GenericTexture('temp/' + urlparse(songLogo).path.split('/')[-1])
    
    # Songdesc ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Starts writing the songdesc (you NEED to use utf-8, 'cause every other breaks the game)
    arq = open("output" + "//" + jsonMapName + "//songdesc.tpl.ckd", "w", encoding='utf-8')
    arq.write('{"__class": "Actor_Template","WIP": 0,"LOWUPDATE": 0,"UPDATE_LAYER": 0,"PROCEDURAL": 0,"STARTPAUSED": 0,"FORCEISENVIRONMENT": 0,"COMPONENTS": [{"__class": "JD_SongDescTemplate","MapName": "' + jsonMapName + '","JDVersion": 2017,"OriginalJDVersion": 2023,"Artist": "' + jsonArtist + '","DancerName": "Unknown Dancer","Title": "' + jsonTitle + '","Credits": "' + jsonCredits.replace("\r\n", " ") + '","PhoneImages": {')
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
    arq.write('"Difficulty": ' + str(jsonDifficulty) + ',')
    arq.write('"Energy": ' + str(jsonSweatDifficulty) + ',')
    arq.write('"backgroundType": 0,"LyricsType": 0,"Tags": ["main"],"Status": 3,"LocaleID": 4294967295,"MojoValue": 0,"CountInProgression": 1,"DefaultColors":{"songcolor_2a": [1, 0.666667, 0.666667, 0.666667],  "lyrics": [1, ' + str(hex2RGB(jsonLyricsColor)[0]/255) + ', ' +  str(hex2RGB(jsonLyricsColor)[1]/255) + ', ' +  str(hex2RGB(jsonLyricsColor)[2]/255) + '], "theme": [1, 1, 1, 1],"songcolor_1a":  [1, 0.266667, 0.266667, 0.266667],"songcolor_2b": [1, 0.466667, 0.466667, 0.466667],"songcolor_1b": [1, 0.066667, 0.066667, 0.066667]},"Paths": {"Avatars": null,"AsyncPlayers": null}}]}')
    arq.close()
    
    # Clean 'temp' folder
    shutil.rmtree('temp')

### Options menu 
if __name__=='__main__':
    while(True):
    
        # Checks if the user is using Windows or Linux as a operating system
        if (sys.platform == "win32"):
            os.system('cls')
        elif (sys.platform == "linux" or sys.platform == "darwin" or sys.platform == "macos"):
            os.system('clear')
        
        print("How're you doing?")
        print("Welcome to WodsonKun's Next2UAF!")
        print("Select a option:")
        print("-----------------------------")
        print("[1] Convert a local Just Dance Next routine to UAF")
        print("[2] Converts a MapPackage bundle to UAF")
        print("[3] Extracts a TexturesLarge bundle")
        print("[4] Extracts a TexturesPhone bundle")
        print("[5] Extracts a SongLogo / Cover1024 / CoverSmall / Cover bundle")
        print("[6] Downloads textures and songdesc from SongDB")
        print("[0] Exits the Next2UAF")
        print("-----------------------------")
        print("\n\nNote: Option 1 converts only MapPackage, TextureLarge and TexturePhone\nOther texture files, taken from the SongDB or from Just Dance Helper\nShould be converted on their specific options")
        
        option = ''
        try:
            option = int(input('Choose your option: '))
        except:
            print('')
        
        # Converts a JDNEXT routine to a UbiArt one
        if option == 1:
            CONV_MapPackage()
            
            # Loads Unity bundles...
            openFile = Tk()
            openFile.title('')
            texturesLargeBundle = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your CoachesLarge BUNDLE file", filetypes=[("Just Dance Next BUNDLE", "*")] )
            texturesPhoneBundle = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your CoachesSmall BUNDLE file", filetypes=[("Just Dance Next BUNDLE", "*")] )
            openFile.destroy()
            
            # Extracts textures
            EXT_TextureLarge(texturesLargeBundle)
            EXT_TexturePhone(texturesPhoneBundle)
        
        # Converts MapPackage stuff to UAF format
        if option == 2:
            CONV_MapPackage()
        
        # Extracts TexturesLarge bundle files
        if option == 3:
            # Asks for the codename
            jsonCodename = input(str('Type the codename of the song: '))
            
            # Loads Unity bundles...
            openFile = Tk()
            openFile.title('')
            texturesLargeBundle = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your CoachesLarge BUNDLE file", filetypes=[("Just Dance Next BUNDLE", "*")] )
            openFile.destroy()
            
            # Extracts phone textures
            EXT_TextureLarge(texturesLargeBundle)
        
        # Extracts TexturesPhone bundle files
        if option == 4:
            # Asks for the codename
            jsonCodename = input(str('Type the codename of the song: '))
            
            # Loads Unity bundles...
            openFile = Tk()
            openFile.title('')
            texturesPhoneBundle = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your CoachesSmall BUNDLE file", filetypes=[("Just Dance Next BUNDLE", "*")] )
            openFile.destroy()
            
            # Extracts phone textures
            EXT_TexturePhone(texturesPhoneBundle)
        
        # Extracts generic texture bundle files
        if (option == 5):
            # Asks for the codename
            jsonCodename = input(str('Type the codename of the song: '))
            
            # Loads Unity bundles...
            openFile = Tk()
            openFile.title('')
            genericTextureBundle = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your Texture BUNDLE file", filetypes=[("Just Dance Next BUNDLE", "*")] )
            openFile.destroy()
            
            # Extracts the textures
            EXT_GenericTexture(genericTextureBundle)
        
        if (option == 6):
            # Asks for the codename
            jsonCodename = input(str('Type the codename of the song: '))
            Plus2UAF()
        
        # Exits the tool
        if option == 0:
            print('Thanks for using our Next2UAF!')
            exit()
        
        else:
            print('Wrong option! Please, choose a valid option')