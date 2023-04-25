import os, sys, io, time, json, struct, pathlib, shutil
from tkinter import *
from tkinter import filedialog

def dec_tml(tml_file):
    f = open(tml_file, "rb")
    f.read(56)
    mapnamelenght = struct.unpack('>I',f.read(4))[0]
    mapname = f.read(mapnamelenght).decode("utf-8")
    f.read(76)
    entries = struct.unpack('>I',f.read(4))[0]
    for e in range(entries):
        e_entryoffset = struct.unpack('>I',f.read(4))[0]
        e_unknown1 = struct.unpack('>I',f.read(4))[0]
        e_unknown2 = struct.unpack('>I',f.read(4))[0]
        e_unknown3 = struct.unpack('>I',f.read(4))[0]
        e_unknown4 = struct.unpack('>I',f.read(4))[0]
        e_unknown5 = struct.unpack('>I',f.read(4))[0]
        e_unknown6 = struct.unpack('>I',f.read(4))[0]
        e_unknown7 = struct.unpack('>I',f.read(4))[0]
        e_unknown8 = struct.unpack('>I',f.read(4))[0]
        e_unknown9 = struct.unpack('>I',f.read(4))[0]
        e_unknown10 = struct.unpack('>I',f.read(4))[0]

    entry_id = 1

    dtape = open("raw_dtape.dec", "w")
    pictoentries = struct.unpack('>I',f.read(4))[0]
    dtape.write('{')
    dtape.write('"__class":"Tape",')
    dtape.write('"Clips":[')
    for pe in range(pictoentries):
        pe_classtype = struct.unpack('>I',f.read(4))[0]
        pe_starttime = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24
        pe_pictonamelenght = struct.unpack('>I',f.read(4))[0]
        pe_pictoname = f.read(pe_pictonamelenght).decode("utf-8")
        pe_isActive = struct.unpack('>I',f.read(4))[0]
        pe_pictopathlenght = struct.unpack('>I',f.read(4))[0]
        pe_pictopath = f.read(pe_pictopathlenght).decode("utf-8")
        pe_pictofilelenght = struct.unpack('>I',f.read(4))[0]
        pe_pictofile = f.read(pe_pictofilelenght).decode("utf-8")
        pe_fileid = struct.unpack('>I',f.read(4))[0]
        pe_useless1 = struct.unpack('>I',f.read(4))[0]#useless

        entry_starttime = round(pe_starttime * 24)

        dtape.write("{")
        dtape.write('"__class":"PictogramClip",')
        dtape.write('"Id":' +  str(entry_id) + ',')
        dtape.write('"TrackId":1,')
        dtape.write('"IsActive":1,')
        dtape.write('"StartTime":' + str(entry_starttime) + ',')
        dtape.write('"Duration":24,')
        dtape.write('"PictoPath":"' + pe_pictopath.replace("jd5", "maps") + pe_pictofile + '",')
        dtape.write('"MontagePath": "", "AtlIndex": 4294967295,')
        dtape.write('"CoachCount":4294967295')
        dtape.write('},')
        entry_id = entry_id + 1
        
    moveentries = struct.unpack('>I',f.read(4))[0]
    total = moveentries
    for me in range(moveentries):
        me_classtype = struct.unpack('>I',f.read(4))[0]
        me_movenamelenght = struct.unpack('>I',f.read(4))[0]
        me_movename = f.read(me_movenamelenght).decode("utf-8")
        me_coachid = struct.unpack('>I',f.read(4))[0]
        me_movepathlenght = struct.unpack('>I',f.read(4))[0]
        me_movepath = f.read(me_movepathlenght).decode("utf-8")
        me_movefilelenght = struct.unpack('>I',f.read(4))[0]
        me_movefile = f.read(me_movefilelenght).decode("utf-8")
        me_fileid = struct.unpack('>I',f.read(4))[0]
        me_useless1 = struct.unpack('>I',f.read(4))[0]#useless
        me_starttime = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24
        me_duration = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24 and subtracted from starttime
        me_goldmove = struct.unpack('>I',f.read(4))[0]
        me_useless2 = struct.unpack('>I',f.read(4))[0]#useless
        me_useless3 = struct.unpack('>I',f.read(4))[0]#useless
        me_useless4 = struct.unpack('>I',f.read(4))[0]#useless

        entry_starttime = round(me_starttime * 24)
        entry_duration = round(me_duration * 24) - entry_starttime

        dtape.write("{")
        dtape.write('"__class":"MotionClip",')
        dtape.write('"Id":' +  str(entry_id) + ',')
        dtape.write('"TrackId":1,')
        dtape.write('"IsActive":1,')
        dtape.write('"StartTime":' + str(entry_starttime) + ',')
        dtape.write('"Duration":' + str(entry_duration) + ',')
        dtape.write('"ClassifierPath":"' + me_movepath.replace("jd5", "maps") + me_movefile + '",')
        dtape.write('"GoldMove":' + str(me_goldmove) + ',')
        dtape.write('"CoachId":' + str(me_coachid) + ',')
        dtape.write('"MoveType":0,')
        dtape.write('"Color":[')
        dtape.write('1,')
        dtape.write('0.968628,')
        dtape.write('0.164706,')
        dtape.write('0.552941')
        dtape.write('],')
        dtape.write('"MotionPlatformSpecifics":{')
        dtape.write('"X360":{')
        dtape.write('"__class":"MotionPlatformSpecific",')
        dtape.write('"ScoreScale":1,')
        dtape.write('"ScoreSmoothing":0,')
        dtape.write('"ScoringMode":0')
        dtape.write('},')
        dtape.write('"ORBIS":{')
        dtape.write('"__class":"MotionPlatformSpecific",')
        dtape.write('"ScoreScale":1,')
        dtape.write('"ScoreSmoothing":0,')
        dtape.write('"ScoringMode":0')
        dtape.write('},')
        dtape.write('"DURANGO":{')
        dtape.write('"__class":"MotionPlatformSpecific",')
        dtape.write('"ScoreScale":1,')
        dtape.write('"ScoreSmoothing":0,')
        dtape.write('"ScoringMode":0')
        dtape.write('}')
        dtape.write('}')
        dtape.write('},')
        entry_id = entry_id + 1

    gestureentries = struct.unpack('>I',f.read(4))[0]
    for ge in range(gestureentries):
        ge_classtype = struct.unpack('>I',f.read(4))[0]
        ge_gesturenamelenght = struct.unpack('>I',f.read(4))[0]
        ge_gesturename = f.read(ge_gesturenamelenght).decode("utf-8")
        ge_coachid = struct.unpack('>I',f.read(4))[0]
        ge_gesturepathlenght = struct.unpack('>I',f.read(4))[0]
        ge_gesturepath = f.read(ge_gesturepathlenght).decode("utf-8")
        ge_gesturefilelenght = struct.unpack('>I',f.read(4))[0]
        ge_gesturefile = f.read(ge_gesturefilelenght).decode("utf-8")
        ge_fileid = struct.unpack('>I',f.read(4))[0]
        ge_useless1 = struct.unpack('>I',f.read(4))[0]#useless
        ge_starttime = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24
        ge_duration = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24 and subtracted from starttime
        ge_goldmove = struct.unpack('>I',f.read(4))[0]
        ge_useless2 = struct.unpack('>I',f.read(4))[0]#useless
        ge_useless3 = struct.unpack('>I',f.read(4))[0]#useless
        ge_useless4 = struct.unpack('>I',f.read(4))[0]#useless

        entry_starttime = round(ge_starttime * 24)
        entry_duration = round(ge_duration * 24) - entry_starttime

        dtape.write("{")
        dtape.write('"__class":"MotionClip",')
        dtape.write('"Id":' +  str(entry_id) + ',')
        dtape.write('"TrackId":1,')
        dtape.write('"IsActive":1,')
        dtape.write('"StartTime":' + str(entry_starttime) + ',')
        dtape.write('"Duration":' + str(entry_duration) + ',')
        dtape.write('"ClassifierPath":"' + ge_gesturepath.replace("jd5", "maps") + ge_gesturefile + '",')
        dtape.write('"GoldMove":' + str(ge_goldmove) + ',')
        dtape.write('"CoachId":' + str(ge_coachid) + ',')
        dtape.write('"MoveType":1,')
        dtape.write('"Color":[')
        dtape.write('1,')
        dtape.write('0.968628,')
        dtape.write('0.164706,')
        dtape.write('0.552941')
        dtape.write('],')
        dtape.write('"MotionPlatformSpecifics":{')
        dtape.write('"X360":{')
        dtape.write('"__class":"MotionPlatformSpecific",')
        dtape.write('"ScoreScale":1,')
        dtape.write('"ScoreSmoothing":0,')
        dtape.write('"ScoringMode":0')
        dtape.write('},')
        dtape.write('"ORBIS":{')
        dtape.write('"__class":"MotionPlatformSpecific",')
        dtape.write('"ScoreScale":2.500000,')
        dtape.write('"ScoreSmoothing":1,')
        dtape.write('"ScoringMode":0')
        dtape.write('},')
        dtape.write('"DURANGO":{')
        dtape.write('"__class":"MotionPlatformSpecific",')
        dtape.write('"ScoreScale":0.750000,')
        dtape.write('"ScoreSmoothing":5,')
        dtape.write('"ScoringMode":0')
        dtape.write('}')
        dtape.write('}')
        dtape.write('},')
        entry_id = entry_id + 1

    
    entry_kid = 1
    ktape = open("raw_ktape.dec", "w", encoding='utf8')
    ktape.write('{')
    ktape.write('"__class":"Tape",')
    ktape.write('"Clips":[')
    
    lyricsentries = struct.unpack('>I',f.read(4))[0]
    total = lyricsentries
    for le in range(lyricsentries):
        le_classtype = struct.unpack('>I',f.read(4))[0]
        le_lyricstextlenght = struct.unpack('>I',f.read(4))[0]
        le_lyricstext = f.read(le_lyricstextlenght).decode("utf-8")
        le_useless1 = struct.unpack('>I',f.read(4))[0]#useless
        le_islineending = struct.unpack('>I',f.read(4))[0]
        le_starttime = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24
        le_duration = struct.unpack('>f',f.read(4))[0]#have to be multiplied be 24 and subtracted from starttime

        entry_starttime = round(le_starttime * 24)
        entry_duration = round(le_duration * 24) - entry_starttime    

        ktape.write("{")
        ktape.write('"__class":"KaraokeClip",')
        ktape.write('"Id":' +  str(entry_kid) + ',')
        ktape.write('"TrackId":1,')
        ktape.write('"IsActive":1,')
        ktape.write('"StartTime":' + str(entry_starttime) + ',')
        ktape.write('"Duration":' + str(entry_duration) + ',')
        ktape.write('"Pitch":8.661958,')
        ktape.write('"Lyrics":"' + le_lyricstext + '",')
        ktape.write('"IsEndOfLine":' + str(le_islineending) + ',')
        ktape.write('"ContentType":0,"StartTimeTolerance":4,"EndTimeTolerance":4,"SemitoneTolerance":5')
        entry_kid = entry_kid + 1
        if(total == 1):
            ktape.write('}')
        else:
            ktape.write('},')
        total = total - 1

    ktape.write('],')
    ktape.write('"TapeClock":0,')
    ktape.write('"TapeBarCount":1,')
    ktape.write('"FreeResourcesAfterPlay":0,')
    ktape.write('"MapName":"' + mapname + '"')
    ktape.write('}')  
    ktape.close()
    
    evententries = struct.unpack('>I',f.read(4))[0]
    gms = []
    gmduration = {}
    for ee in range(evententries):
        ee_eventtype = struct.unpack('>I',f.read(4))[0]
        if(ee_eventtype == 1039419589):
            f.read(17)
            continue
        ee_useless1 = struct.unpack('>I',f.read(4))[0]
        if(ee_useless1 != 0):
            f.read(ee_useless1 + 86)
        else:
            ee_starttime = struct.unpack('>f',f.read(4))[0]
            ee_duration = struct.unpack('>f',f.read(4))[0]
            ee_useless2 = struct.unpack('>I',f.read(4))[0]
            ee_eventnamelenght = struct.unpack('>I',f.read(4))[0]
            ee_eventname = f.read(ee_eventnamelenght).decode("utf-8")
            if(ee_eventname == "eventdelayeve"):
                f.read(197)
            if(ee_eventname == "tag"):
                f.read(67)
            if(ee_eventname == "eventmultieve"):
                f.read(107)
            if(ee_eventname == "playsnd"):
                f.read(39)
            if(ee_eventname == "event_fadingmaterial"):
                f.read(370)
            if(ee_eventname == "bpm"):
                f.read(20)
            if(ee_eventname == "karaokescoring"):
                f.read(8)
            if(ee_eventname == "goldmove"):
                f.read(16)
                ee_othereventnamelenght = struct.unpack('>I',f.read(4))[0]
                ee_othereventname = f.read(ee_othereventnamelenght).decode("utf-8")

                entry_starttime = round(ee_starttime * 24)
                entry_duration = round(ee_duration * 24) - entry_starttime
                
                gms.append(entry_starttime)
                gmduration.update({entry_starttime: entry_duration})
                
            if(ee_eventname == "goldmovecascade"):
                f.read(4)
                ee_othereventnamelenght = struct.unpack('>I',f.read(4))[0]
                ee_othereventname = f.read(ee_othereventnamelenght).decode("utf-8")

                entry_starttime = round(ee_starttime * 24)
                entry_duration = round(ee_duration * 24) - entry_starttime
                
                gms.append(entry_starttime)
                gmduration.update({entry_starttime: entry_duration})
                

    total = len(gms)
    for goldframe in range(len(gms)):
        entry_starttime = gms[goldframe]
        entry_duration = gmduration[entry_starttime]
        dtape.write("{")
        dtape.write('"__class":"GoldEffectClip",')
        dtape.write('"Id":' +  str(entry_id) + ',')
        dtape.write('"TrackId":1,')
        dtape.write('"IsActive":1,')
        dtape.write('"StartTime":' + str(entry_starttime) + ',')
        dtape.write('"Duration":' + str(entry_duration) + ',')
        dtape.write('"EffectType":0')
        entry_id = entry_id + 1
        if(total == 1):
            dtape.write('}')
        else:
            dtape.write('},')
        total = total - 1
        
    dtape.write('],')
    dtape.write('"TapeClock":0,')
    dtape.write('"TapeBarCount":1,')
    dtape.write('"FreeResourcesAfterPlay":0,')
    dtape.write('"MapName":"' + mapname + '"')
    dtape.write('}') 
    dtape.close()
    f.close()
    
    # Creates output folder
    try:
        os.mkdir("output//" + mapname) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada
    
    # Loads the old DTAPE into memory and then deletes it
    dtapejson = json.load(open("raw_dtape.dec", "r"))
    os.remove("raw_dtape.dec")
    
    # Fixes CoachId issue
    oldcoachid = []
    fixcoachid = {}
    gestoldcoachid = []
    gestfixcoachid = {}
    for mv in dtapejson['Clips']:
        if(mv['__class'] == "MotionClip" and mv['MoveType'] == 0):
            if(mv['CoachId'] not in oldcoachid):
                oldcoachid.append(mv['CoachId'])
    oldcoachid = sorted(oldcoachid, key=int)
    
    for x in range(len(oldcoachid)):
        fixcoachid.update({oldcoachid[x]: x})
        
    for mv in dtapejson['Clips']:
        if(mv['__class'] == "MotionClip" and mv['MoveType'] == 0):
            mv['CoachId'] = fixcoachid[mv['CoachId']]
            
    for mv in dtapejson['Clips']:
        if(mv['__class'] == "MotionClip" and mv['MoveType'] == 1):
            if(mv['CoachId'] not in gestoldcoachid):
                gestoldcoachid.append(mv['CoachId'])
    gestoldcoachid = sorted(gestoldcoachid, key=int)
    
    for x in range(len(gestoldcoachid)):
        gestfixcoachid.update({gestoldcoachid[x]: x})
        
    for mv in dtapejson['Clips']:
        if(mv['__class'] == "MotionClip" and mv['MoveType'] == 1):
            mv['CoachId'] = gestfixcoachid[mv['CoachId']]
    
    fixdtape = open("raw_dtape.dec", "w")
    fixdtape.write(str(dtapejson).replace("'", '"'))
    fixdtape.close()
    
    # Moves DTAPE and KTAPE to output folder
    shutil.move("raw_ktape.dec", "output" + "//" + mapname + "//" + mapname.lower() + "_tml_karaoke.ktape.ckd")
    shutil.move("raw_dtape.dec", "output" + "//" + mapname + "//" + mapname.lower() + "_tml_dance.dtape.ckd")

def dec_dtape():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    dtapefile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your DTAPE file", filetypes=[("DTAPE (.ktape.ckd)", "*.dtape.ckd")] )
    
    # Abre e lê o JSON
    f = open(dtapefile, "rb")
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Asks for codename
    entry_mapname = str(input('Type the codename of the song: '))
    
    arq = open("raw_dtape.dec", "w")
    arq.write('{')
    arq.write('"__class":"Tape",')
    arq.write('"Clips":[')
    #Header
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)#timeline ver
    timeline_ver = struct.unpack('>I', byte)[0]
    #Header
    #Infos
    byte = f.read(4)#Entries
    entries = struct.unpack('>I', byte)[0]
    total = entries
    #Infos
    for x in range(entries):
        byte = f.read(4)#unknown
        entry_unknown = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#class_id
        entry_class = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#id
        entry_id = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#trackid
        entry_trackid = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#isactive
        entry_isactive = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#starttime
        entry_starttime = struct.unpack('>I', byte)[0]

        byte = f.read(4)#duration
        entry_duration = struct.unpack('>I', byte)[0]
        
        if(entry_class == 108 or entry_class == 112 or entry_class == 56):
            byte = f.read(4)#namelength
            entry_namelength = struct.unpack('>I', byte)[0]

            byte = f.read(entry_namelength)#name
            entry_name = byte.decode("utf-8")

            byte = f.read(4)#pathlength
            entry_pathlength = struct.unpack('>I', byte)[0]

            byte = f.read(entry_pathlength)#path
            entry_path = byte.decode("utf-8")

            byte = f.read(4)#atlindex
            entry_atlindex = struct.unpack('>I', byte)[0]

            byte = f.read(4)#unknown2
            entry_unknown2 = struct.unpack('>I', byte)[0]
            
            if(entry_class == 108 or entry_class == 112):

                byte = f.read(4)#goldmove
                entry_goldmove = struct.unpack('>I', byte)[0]

                byte = f.read(4)#coachid
                entry_coachid = struct.unpack('>I', byte)[0]

                byte = f.read(4)#movetype
                entry_movetype = struct.unpack('>I', byte)[0]
                #Useless stuff
                #Colors
                byte = f.read(4)#color1
                byte = f.read(4)#color2
                byte = f.read(4)#color3
                byte = f.read(4)#color4
                #Colors
                #Pointing
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                byte = f.read(4)
                #Useless stuff
                arq.write("{")
                arq.write('"__class":"MotionClip",')
                arq.write('"Id":' +  str(entry_id) + ',')
                arq.write('"TrackId":' + str(entry_trackid) + ',')
                arq.write('"IsActive":' + str(entry_isactive) + ',')
                arq.write('"StartTime":' + str(entry_starttime) + ',')
                arq.write('"Duration":' + str(entry_duration) + ',')
                arq.write('"ClassifierPath":"' + entry_path.replace("jd2015", "maps") + entry_name + '",')
                arq.write('"GoldMove":' + str(entry_goldmove) + ',')
                arq.write('"CoachId":' + str(entry_coachid) + ',')
                arq.write('"MoveType":' + str(entry_movetype) + ',')
                arq.write('"Color":[')
                arq.write('1,')
                arq.write('0.968628,')
                arq.write('0.164706,')
                arq.write('0.552941')
                arq.write('],')
                arq.write('"MotionPlatformSpecifics":{')
                arq.write('"X360":{')
                arq.write('"__class":"MotionPlatformSpecific",')
                arq.write('"ScoreScale":1,')
                arq.write('"ScoreSmoothing":0,')
                arq.write('"ScoringMode":0')
                arq.write('},')
                arq.write('"ORBIS":{')
                arq.write('"__class":"MotionPlatformSpecific",')
                arq.write('"ScoreScale":1,')
                arq.write('"ScoreSmoothing":0,')
                arq.write('"ScoringMode":0')
                arq.write('},')
                arq.write('"DURANGO":{')
                arq.write('"__class":"MotionPlatformSpecific",')
                arq.write('"ScoreScale":1,')
                arq.write('"ScoreSmoothing":0,')
                arq.write('"ScoringMode":0')
                arq.write('}')
                arq.write('}')
            elif(entry_class == 56):
                byte = f.read(4)#coachcount
                entry_coachcount = struct.unpack('>I', byte)[0]
                arq.write("{")
                arq.write('"__class":"PictogramClip",')
                arq.write('"Id":' +  str(entry_id) + ',')
                arq.write('"TrackId":' + str(entry_trackid) + ',')
                arq.write('"IsActive":' + str(entry_isactive) + ',')
                arq.write('"StartTime":' + str(entry_starttime) + ',')
                arq.write('"Duration":' + str(entry_duration) + ',')
                arq.write('"PictoPath":"' + entry_path.replace("jd2015", "maps") + entry_name + '",')
                arq.write('"CoachCount":' + str(entry_coachcount))    
        elif(entry_class == 28):
            byte = f.read(4)#effecttype
            entry_effecttype = struct.unpack('>I', byte)[0]
            arq.write("{")
            arq.write('"__class":"GoldEffectClip",')
            arq.write('"Id":' +  str(entry_id) + ',')
            arq.write('"TrackId":' + str(entry_trackid) + ',')
            arq.write('"IsActive":' + str(entry_isactive) + ',')
            arq.write('"StartTime":' + str(entry_starttime) + ',')
            arq.write('"Duration":' + str(entry_duration) + ',')
            arq.write('"EffectType":' + str(entry_effecttype))
        else:
            print("New entry class found:", entry_class)
        if(total == 1):
            arq.write('}')
        else:
            arq.write('},')
        total = total - 1
    
    arq.write('],')
    arq.write('"TapeClock":0,')
    arq.write('"TapeBarCount":1,')
    arq.write('"FreeResourcesAfterPlay":0,')
    arq.write('"MapName":"' + entry_mapname + '"')
    arq.write('}')
    f.close()
    arq.close()
    
    # Creates output folder
    try:
        os.mkdir("output//" + entry_mapname) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada
    
    # Moves DTAPE to output folder
    shutil.move("raw_dtape.dec", "output" + "//" + entry_mapname + "//" + entry_mapname.lower() + "_tml_dance.dtape.ckd")
 
#KTAPE
def dec_ktape():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    ktapefile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your KTAPE file", filetypes=[("KTAPE (.ktape.ckd)", "*.ktape.ckd")] )
    
    # Abre e lê o JSON
    f = open(ktapefile, "rb")
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Asks for codename
    entry_mapname = str(input('Type the codename of the song: '))
    
    arq = open("raw_ktape.dec", "w", encoding="utf8")
    arq.write('{')
    arq.write('"__class":"Tape",')
    arq.write('"Clips":[')
    #Header
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)#timeline ver
    timeline_ver = struct.unpack('>I', byte)[0]
    #Header
    #Infos
    byte = f.read(4)#Entries
    entries = struct.unpack('>I', byte)[0]
    total = entries
    #Infos
    for x in range(entries):
        byte = f.read(4)#unknown
        entry_unknown = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#class_id
        entry_class = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#id
        entry_id = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#trackid
        entry_trackid = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#isactive
        entry_isactive = struct.unpack('>I', byte)[0]
        
        byte = f.read(4)#starttime
        entry_starttime = struct.unpack('>I', byte)[0]

        byte = f.read(4)#duration
        entry_duration = struct.unpack('>I', byte)[0]

        byte = f.read(4)#pitch
        entry_pitch = struct.unpack('>f', byte)[0]

        byte = f.read(4)#lyricslength
        entry_lyricslength = struct.unpack('>I', byte)[0]

        byte = f.read(entry_lyricslength)#lyrics
        entry_lyrics = byte.decode("utf-8")

        byte = f.read(4)#isendofline
        entry_isendofline = struct.unpack('>I', byte)[0]

        #Maybe some kind of karaoke pointing shit
        byte = f.read(4)
        byte = f.read(4)
        byte = f.read(4)
        byte = f.read(4)

        arq.write("{")
        arq.write('"__class":"KaraokeClip",')
        arq.write('"Id":' +  str(entry_id) + ',')
        arq.write('"TrackId":' + str(entry_trackid) + ',')
        arq.write('"IsActive":' + str(entry_isactive) + ',')
        arq.write('"StartTime":' + str(entry_starttime) + ',')
        arq.write('"Duration":' + str(entry_duration) + ',')
        arq.write('"Pitch":' + str(entry_pitch) + ',')
        arq.write('"Lyrics":"' + entry_lyrics + '",')
        arq.write('"IsEndOfLine":' + str(entry_isendofline) + ',')
        arq.write('"ContentType":0,"StartTimeTolerance":4,"EndTimeTolerance":4,"SemitoneTolerance":5')
        if(total == 1): 
            arq.write('}')
        else:
            arq.write('},')
        total = total - 1

    arq.write('],')
    arq.write('"TapeClock":0,')
    arq.write('"TapeBarCount":1,')
    arq.write('"FreeResourcesAfterPlay":0,')
    arq.write('"MapName":"' + entry_mapname + '"')
    arq.write('}')
    f.close()
    arq.close()
    
    # Creates output folder
    try:
        os.mkdir("output//" + entry_mapname) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada
    
    # Moves DTAPE and KTAPE to output folder
    shutil.move("raw_ktape.dec", "output" + "//" + entry_mapname + "//" + entry_mapname.lower() + "_tml_karaoke.ktape.ckd")

# Songdesc (from Just Dance 2014 and Just Dance 2015)
def dec_sd_14():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    sdfile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your Songdesc file", filetypes=[("Songdesc (.tpl.ckd)", "*.tpl.ckd")] )
    
    # Abre e lê o JSON
    f = open(sdfile, "rb")
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Reads and deserializes the songdesc
    entry_mapnamealtsd = None
    f.read(56)
    entry_mpnamelengthsd = struct.unpack('>I', f.read(4))[0]
    entry_mapnamesd = f.read(entry_mpnamelengthsd).decode("utf-8")
    f.read(4)
    entry_isalt = struct.unpack('>I', f.read(4))[0]
    if(entry_isalt == 1):
        entry_mpnamealtlengthsd = struct.unpack('>I', f.read(4))[0]
        entry_mapnamealtsd = f.read(entry_mpnamealtlengthsd).decode("utf-8")
    entry_messquantity = struct.unpack('>I', f.read(4))[0]
    if(entry_messquantity == 1 or entry_messquantity == 2):
        for x in range(entry_messquantity):
            f.read(44)
    if(entry_messquantity == 3):
        f.read(48)
        entry_messinside = struct.unpack('>I', f.read(4))[0]
        if(entry_messinside == 1):
            f.read(120)
        else:
            f.read(80)
    entry_artistlengthsd = struct.unpack('>I', f.read(4))[0]
    entry_artistsd = f.read(entry_artistlengthsd).decode("utf-8")
    entry_titlelengthsd = struct.unpack('>I', f.read(4))[0]
    entry_titlesd = f.read(entry_titlelengthsd).decode("utf-8")
    entry_numcoach = struct.unpack('>I', f.read(4))[0]
    if(entry_isalt != 1):
        f.read(24)
        entry_previewentry = struct.unpack('>I', f.read(4))[0]
        f.read(12)
        entry_previewLoopStart = struct.unpack('>I', f.read(4))[0]
        entry_previewLoopEnd = struct.unpack('>I', f.read(4))[0]
        f.read(8)
    else:
        f.read(24)
        entry_previewentry = 0
        entry_previewLoopStart = 0
        entry_previewLoopEnd = 100
    entry_lyricscolor3 = struct.unpack('>f', f.read(4))[0]
    entry_lyricscolor2 = struct.unpack('>f', f.read(4))[0]
    entry_lyricscolor1 = struct.unpack('>f', f.read(4))[0]
    entry_lyricscolor0 = struct.unpack('>f', f.read(4))[0]
    
    # Creates output folder
    try:
        os.mkdir("output//" + entry_mapnamesd) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada
    
    # Starts writing the songdesc
    arq = open("output" + "//" + entry_mapnamesd + "//songdesc.tpl.ckd", "w", encoding='utf-8')
    arq.write('''{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"JD_SongDescTemplate","MapName":"''' + entry_mapnamesd + '''","JDVersion":2017,"OriginalJDVersion":2014,"Artist":"''' + entry_artistsd + '''","DancerName":"Unknown Dancer","Title":"''' + entry_titlesd + '''","Credits": "All rights of the producer and other rightholders to the recorded work reserved. Unless otherwise authorized, the duplication, rental, loan, exchange or use of this video game for public performance, broadcasting and online distribution to the public are prohibited.", "PhoneImages": {''')
    arq.write('"Cover": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_cover_phone.jpg",')
    if (entry_numcoach == 1):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png"')
    elif (entry_numcoach == 2):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_2_phone.png"')
    elif (entry_numcoach == 3):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_3_phone.png"')
    elif (entry_numcoach == 4):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_3_phone.png", "coach4": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_4_phone.png"')
    arq.write('},')
    arq.write('''"NumCoach":''' + str(entry_numcoach) + ''',"MainCoach":-1,"Difficulty":2,"SweatDifficulty":2,"backgroundType":0,"LyricsType":0,"Tags":["main"],"Status":3,"LocaleID":4294967295,"MojoValue":0,"CountInProgression":1,"DefaultColors":{"songcolor_2a":[0, 0, 0, 0],"lyrics":[''' + str(entry_lyricscolor0) + ''', ''' + str(entry_lyricscolor1) + ''', ''' + str(entry_lyricscolor2) + ''', ''' + str(entry_lyricscolor3) + '''],"theme":[1, 1, 1, 1],"songcolor_1a":[0, 0, 0, 0],"songcolor_2b":[0, 0, 0, 0],"songcolor_1b":[0, 0, 0, 0]},"VideoPreviewPath":""}]}''')
    arq.close()
    f.close()
    #return sdjson, entry_previewentry, entry_previewLoopStart, entry_previewLoopEnd, entry_mapnamealtsd

def dec_sd_15():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    sdfile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your Songdesc file", filetypes=[("Songdesc (.tpl.ckd)", "*.tpl.ckd")] )
    
    # Abre e lê o JSON
    f = open(sdfile, "rb")
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Reads and deserializes the songdesc
    entry_mapnamealtsd = None
    f.read(56)
    entry_mpnamelengthsd = struct.unpack('>I', f.read(4))[0]
    entry_mapnamesd = f.read(entry_mpnamelengthsd).decode("utf-8")
    f.read(8)
    entry_isalt = struct.unpack('>I', f.read(4))[0]
    if(entry_isalt == 1):
        entry_mpnamealtlengthsd = struct.unpack('>I', f.read(4))[0]
        entry_mapnamealtsd = f.read(entry_mpnamealtlengthsd).decode("utf-8")
    entry_messquantity = struct.unpack('>I', f.read(4))[0]
    f.read(16)
    entry_localeid = struct.unpack('>I', f.read(4))[0]
    f.read(32)
    if(entry_messquantity == 2):
        f.read(52)
    entry_artistlengthsd = struct.unpack('>I', f.read(4))[0]
    entry_artistsd = f.read(entry_artistlengthsd).decode("utf-8")
    f.read(18)
    entry_titlelengthsd = struct.unpack('>I', f.read(4))[0]
    entry_titlesd = f.read(entry_titlelengthsd).decode("utf-8")
    entry_numcoach = struct.unpack('>I', f.read(4))[0]
    f.read(4)
    entry_diff = struct.unpack('>I', f.read(4))[0]
    entry_backgroundtype = struct.unpack('>I', f.read(4))[0]
    entry_lyricstype = struct.unpack('>I', f.read(4))[0]
    if(entry_isalt != 1):
        f.read(20)
        entry_previewentry = struct.unpack('>I', f.read(4))[0]
        f.read(12)
        entry_previewLoopStart = struct.unpack('>I', f.read(4))[0]
        entry_previewLoopEnd = struct.unpack('>I', f.read(4))[0]
    else:
        f.read(12)
        entry_previewentry = 0
        entry_previewLoopStart = 0
        entry_previewLoopEnd = 100
    '''
    if(ver == "jd17" or ver == "jd18" or ver == "jd19"):
        f.read(28)
    else:
        f.read(8)
    '''
    f.read(8)
    entry_lyricscolor3 = struct.unpack('>f', f.read(4))[0]
    entry_lyricscolor2 = struct.unpack('>f', f.read(4))[0]
    entry_lyricscolor1 = struct.unpack('>f', f.read(4))[0]
    entry_lyricscolor0 = struct.unpack('>f', f.read(4))[0]
    
    # Creates output folder
    try:
        os.mkdir("output//" + entry_mapnamesd) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada
    
    # Starts writing the songdesc
    arq = open("output" + "//" + entry_mapnamesd + "//songdesc.tpl.ckd", "w", encoding='utf-8')
    arq.write('''{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"JD_SongDescTemplate","MapName":"''' + entry_mapnamesd + '''","JDVersion":2017,"OriginalJDVersion":2015,"Artist":"''' + entry_artistsd + '''","DancerName":"Unknown Dancer","Title":"''' + entry_titlesd + '''","Credits": "All rights of the producer and other rightholders to the recorded work reserved. Unless otherwise authorized, the duplication, rental, loan, exchange or use of this video game for public performance, broadcasting and online distribution to the public are prohibited.", "PhoneImages": {''')
    arq.write('"Cover": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_cover_phone.jpg",')
    if (entry_numcoach == 1):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png"')
    elif (entry_numcoach == 2):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_2_phone.png"')
    elif (entry_numcoach == 3):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_3_phone.png"')
    elif (entry_numcoach == 4):
        arq.write('"coach1": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_1_phone.png", "coach2": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_2_phone.png", "coach3": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_3_phone.png", "coach4": "world/maps/' + entry_mapnamesd.lower() + '/menuart/textures/' + entry_mapnamesd.lower() + '_coach_4_phone.png"')
    arq.write('},')
    arq.write('''"NumCoach":''' + str(entry_numcoach) + ''',"MainCoach":-1,"Difficulty":2,"SweatDifficulty":2,"backgroundType":0,"LyricsType":''' + str(entry_lyricstype) + ''',"Tags":["main"],"Status":3,"LocaleID":''' + str(entry_localeid) + ''',"MojoValue":0,"CountInProgression":1,"DefaultColors":{"songcolor_2a":[0, 0, 0, 0],"lyrics":[''' + str(entry_lyricscolor0) + ''', ''' + str(entry_lyricscolor1) + ''', ''' + str(entry_lyricscolor2) + ''', ''' + str(entry_lyricscolor3) + '''],"theme":[1, 1, 1, 1],"songcolor_1a":[0, 0, 0, 0],"songcolor_2b":[0, 0, 0, 0],"songcolor_1b":[0, 0, 0, 0]},"VideoPreviewPath":""}]}''')
    arq.close()
    f.close()
    #return sdjson, entry_previewentry, entry_previewLoopStart, entry_previewLoopEnd, entry_mapnamealtsd

# Musictrack (from Just Dance 2014 and Just Dance 2015)
def dec_mt_14():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    mt_file = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your Musictrack file", filetypes=[("Musictrack (.tpl.ckd)", "*.tpl.ckd")] )
    
    # Abre e lê o JSON
    f = open(mt_file, "rb")
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Asks for codename
    MTMapName = str(input('Type the codename of the song: '))
    
    # Creates output folder
    try:
        os.mkdir("output//" + MTMapName) # Cria uma pasta com o codename da música do JSON
    except:
        pass # Caso a pasta já exista, ele não faz nada
    
    arq = open("output" + "//" + MTMapName + "//" + MTMapName.lower() + "_musictrack.tpl.ckd", "w")
    arq.write('{')
    arq.write('"__class":"Actor_Template",')
    arq.write('"WIP":0,')
    arq.write('"LOWUPDATE":0,')
    arq.write('"UPDATE_LAYER":0,')
    arq.write('"PROCEDURAL":0,')
    arq.write('"STARTPAUSED":0,')
    arq.write('"FORCEISENVIRONMENT":0,')
    arq.write('"COMPONENTS": [{')
    arq.write('"__class": "MusicTrackComponent_Template",')
    arq.write('"trackData": {')
    arq.write('"__class": "MusicTrackData",')
    arq.write('"structure": {')
    arq.write('"__class": "MusicTrackStructure",')
    #Header
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    #Header

    byte = f.read(4)#Markers
    markers = struct.unpack('>I', byte)[0]
    beats = []
    
    for x in range(markers):
        byte = f.read(4)#beat
        beat = struct.unpack('>I', byte)[0]
        beats.append(beat)
    arq.write('"markers":' + str(beats).replace(" ", "") + ',')

    byte = f.read(4)#signatures
    signatures = struct.unpack('>I', byte)[0]
    arq.write('"signatures": [')    
    for x in range(signatures):
        byte = f.read(4)#class
        byte = f.read(4)#marker
        sig_marker = struct.unpack('>I', byte)[0]
        byte = f.read(4)#beat
        sig_beat = struct.unpack('>I', byte)[0]
        arq.write('{')
        arq.write('"__class": "MusicSignature",')
        arq.write('"marker":' + str(sig_marker) + ',')
        arq.write('"beats":'+ str(sig_beat))
        if(signatures-x == 1):
            arq.write('}')
        else:
            arq.write('},')
    arq.write('],')

    byte = f.read(4)#sections
    sections = struct.unpack('>I', byte)[0]
    arq.write('"sections": [')

    for x in range(sections):
        byte = f.read(4)#class
        byte = f.read(4)#marker
        sec_marker = struct.unpack('>I', byte)[0]
        byte = f.read(4)#sectiontype
        sec_sectiontype = struct.unpack('>I', byte)[0]
        byte = f.read(4)#commentlength
        commentlength = struct.unpack('>I', byte)[0]
        byte = f.read(commentlength)
        arq.write('{')
        arq.write('"__class": "MusicSection",')
        arq.write('"marker":' + str(sec_marker) + ',')
        arq.write('"sectionType":'+ str(sec_sectiontype) + ',')
        arq.write('"comment":""')
        if(sections-x == 1):
            arq.write('}')
        else:
            arq.write('},')
    arq.write('],')
        
    #MUSICTRACK Ending
    byte = f.read(4)#startbeat
    startbeat = struct.unpack('>i', byte)[0]

    byte = f.read(4)#endbeat
    endbeat = struct.unpack('>I', byte)[0]

    byte = f.read(4)#videostarttime
    videostarttime = struct.unpack('>f', byte)[0]

    byte = f.read(4)#pathlength
    wavpathlength = struct.unpack('>I', byte)[0]
    byte = f.read(wavpathlength)
    wavpath = byte.decode("utf-8")
    
    byte = f.read(4)#wavlength
    wavlength = struct.unpack('>I', byte)[0]
    byte = f.read(wavlength)
    wav = byte.decode("utf-8")

    arq.write('"startBeat":' + str(startbeat) + ',')
    arq.write('"endBeat":' + str(endbeat) +',')
    arq.write('"videoStartTime":' + str(videostarttime) + ',')
    arq.write('"previewEntry":' + str(int(endbeat/2)) + ',')
    arq.write('"previewLoopStart":' + str(int(endbeat/2)) + ',')
    arq.write('"previewLoopEnd":' + str(endbeat) + ',')
    arq.write('"volume":0')
    arq.write('},')
    arq.write('"path": "world/maps/' + MTMapName.lower() + '/audio/' + MTMapName.lower() + '.wav", "url": "jmcs://jd-contents/' + MTMapName + '/' + MTMapName + '.ogg"')
    arq.write('}}]}')
    
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    f.close()
    arq.close()

def dec_mt_15():
    # Inicializa o Tkinter (para usar o seletor de arquivos)
    openFile = Tk()
    openFile.title('')
    
    # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
    mt_file = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your Musictrack file", filetypes=[("Musictrack (.tpl.ckd)", "*.tpl.ckd")] )
    
    # Abre e lê o JSON
    f = open(mt_file, "rb")
        
    # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
    openFile.destroy()
    
    # Asks for codename
    MTMapName = str(input('Type the codename of the song: '))
    
    # Creates output folder
    os.makedirs("output//" + MTMapName, exist_ok=True)
    
    arq = open("output" + "//" + MTMapName + "//" + MTMapName.lower() + "_musictrack.tpl.ckd", "w")
    arq.write('{')
    arq.write('"__class":"Actor_Template",')
    arq.write('"WIP":0,')
    arq.write('"LOWUPDATE":0,')
    arq.write('"UPDATE_LAYER":0,')
    arq.write('"PROCEDURAL":0,')
    arq.write('"STARTPAUSED":0,')
    arq.write('"FORCEISENVIRONMENT":0,')
    arq.write('"COMPONENTS": [{')
    arq.write('"__class": "MusicTrackComponent_Template",')
    arq.write('"trackData": {')
    arq.write('"__class": "MusicTrackData",')
    arq.write('"structure": {')
    arq.write('"__class": "MusicTrackStructure",')
    #Header
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)#timeline ver
    timeline_version = struct.unpack('>I', byte)[0]
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    #Header

    byte = f.read(4)#Markers
    markers = struct.unpack('>I', byte)[0]
    beats = []
    
    for x in range(markers):
        byte = f.read(4)#beat
        beat = struct.unpack('>I', byte)[0]
        beats.append(beat)
    arq.write('"markers":' + str(beats).replace(" ", "") + ',')

    byte = f.read(4)#signatures
    signatures = struct.unpack('>I', byte)[0]
    arq.write('"signatures": [')    
    for x in range(signatures):
        byte = f.read(4)#class
        byte = f.read(4)#marker
        sig_marker = struct.unpack('>I', byte)[0]
        byte = f.read(4)#beat
        sig_beat = struct.unpack('>I', byte)[0]
        arq.write('{')
        arq.write('"__class": "MusicSignature",')
        arq.write('"marker":' + str(sig_marker) + ',')
        arq.write('"beats":'+ str(sig_beat))
        if(signatures-x == 1):
            arq.write('}')
        else:
            arq.write('},')
    arq.write('],')

    byte = f.read(4)#sections
    sections = struct.unpack('>I', byte)[0]
    arq.write('"sections": [')

    for x in range(sections):
        byte = f.read(4)#class
        byte = f.read(4)#marker
        sec_marker = struct.unpack('>I', byte)[0]
        byte = f.read(4)#sectiontype
        sec_sectiontype = struct.unpack('>I', byte)[0]
        byte = f.read(4)#commentlength
        commentlength = struct.unpack('>I', byte)[0]
        byte = f.read(commentlength)
        arq.write('{')
        arq.write('"__class": "MusicSection",')
        arq.write('"marker":' + str(sec_marker) + ',')
        arq.write('"sectionType":'+ str(sec_sectiontype) + ',')
        arq.write('"comment":""')
        if(sections-x == 1):
            arq.write('}')
        else:
            arq.write('},')
    arq.write('],')
        
    #MUSICTRACK Ending
    byte = f.read(4)#startbeat
    startbeat = struct.unpack('>i', byte)[0]

    byte = f.read(4)#endbeat
    endbeat = struct.unpack('>I', byte)[0]
    '''
    if(timeline_ver == "jd18" or timeline_ver == "jd19"):
        #UNKNOWN
        byte = f.read(4)
        byte = f.read(6)
        #UNKNOWN
    '''
    byte = f.read(4)#videostarttime
    videostarttime = struct.unpack('>f', byte)[0]
    
    byte = f.read(4)
    
    byte = f.read(4)#wavlength
    wavlength = struct.unpack('>I', byte)[0]
    byte = f.read(wavlength)
    wav = byte.decode("utf-8")

    byte = f.read(4)#pathlength
    wavpathlength = struct.unpack('>I', byte)[0]
    byte = f.read(wavpathlength)
    wavpath = byte.decode("utf-8")

    arq.write('"startBeat":' + str(startbeat) + ',')
    arq.write('"endBeat":' + str(endbeat) +',')
    arq.write('"videoStartTime":' + str(videostarttime) + ',')
    arq.write('"previewEntry":' + str(int(endbeat/2)) + ',')
    arq.write('"previewLoopStart":' + str(int(endbeat/2)) + ',')
    arq.write('"previewLoopEnd":' + str(endbeat) + ',')
    arq.write('"volume":0')
    arq.write('},')
    arq.write('"path": "world/maps/' + MTMapName.lower() + '/audio/' + MTMapName.lower() + '.wav", "url": "jmcs://jd-contents/' + MTMapName + '/' + MTMapName + '.ogg"')
    arq.write('}}]}')
    
    byte = f.read(4)
    byte = f.read(4)
    byte = f.read(4)
    arq.close()
    f.close()

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    while(True):
        os.system('cls')
        print("                                          Welcome to WodsonKun's DeserializerSuite!")
        print("                                                 Credits to augustodoidin")
        print("Select a option:")
        print("-----------------------------")
        print("[1] Deserialize a songdesc from Just Dance 2014 / Just Dance 2015")
        print("[2] Deserializes DTAPE and KTAPE from Just Dance 2014 / Just Dance 2015")
        print("[3] Deserialize a Musictrack from Just Dance 2014 / Just Dance 2015")
        print("[4] Exit the DeserializerSuite")
        print("\n\n\nNote: This tool supports the following games:\n - Just Dance 2014\n - Just Dance Wii U\n - Just Dance Yo-Kai: Special Edition\n - Just Dance 2015\n - Just Dance 2015 (China)")
        print("-----------------------------")
        
        option = input('Enter your choice: ')

        #Check what choice was entered and act accordingly
        if option == "1":
            VerQuestion = input('Are you deserializing from Just Dance 2014 or Just Dance 2015? (2014 or 2015): ')
            if (VerQuestion == "2014"):
                dec_sd_14()
            elif (VerQuestion == "2015"):
                dec_sd_15()
        if option == "2":
            VerQuestion = input('Are you deserializing from Just Dance 2014 or Just Dance 2015? (2014 or 2015): ')
            if (VerQuestion == "2014"):
                # Inicializa o Tkinter (para usar o seletor de arquivos)
                openFile = Tk()
                openFile.title('')
                
                # Procura o JSON principal (apenas ele é usado para gerar a songdesc)
                tml_file = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your Timeline file", filetypes=[("Timeline (.tpl.ckd)", "timeline.tpl.ckd")] )
                    
                # Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
                openFile.destroy()
                
                # Starts deserializing
                dec_tml(tml_file)
            elif (VerQuestion == "2015"):
                dec_dtape()
                dec_ktape()
        if option == "3":
            VerQuestion = input('Are you deserializing from Just Dance 2014 or Just Dance 2015? (2014 or 2015): ')
            if (VerQuestion == "2014"):
                dec_mt_14()
            elif (VerQuestion == "2015"):
                dec_mt_15()
        if option == "4":
            print('Thanks for using our decryptor!')
            time.sleep(2)
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 8.')
            time.sleep(1)