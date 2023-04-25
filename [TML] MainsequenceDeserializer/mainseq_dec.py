import os, sys, io, struct, math, shutil, pathlib, random
from tkinter import *
from tkinter import filedialog

# randomId (por WodsonKun)
def randomId():
    return math.floor(random.randint(0, 40000) * (40000 - 10000 + 1) + 10000) # Gera um valor randômico e retorna o mesmo para ser usado como ID

# Inicializa o Tkinter (para usar o seletor de arquivos)
openFile = Tk()
openFile.title('')

# Procura o JSON principal (apenas ele é usado para gerar a songdesc)
MainSequence = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu JSON", filetypes=[("Mainsequence (.tape.ckd)", "_mainsequence.tape.ckd")])

# Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
openFile.destroy()

# Cria a pasta com o codenome da música
os.makedirs("output//", exist_ok=True)

JDVer = int(input("It's a Just Dance 2014 or Just Dance 2015 mainsequence (2014 or 2015)?: "))

# Abre e lê o JSON (UTF-8-SIG, para idêntificação dos caracteres japoneses, chineses ou coreanos)
f = open(MainSequence, 'rb+')

# Starts writing the deserialized one
arq = open('output//' + os.path.basename(MainSequence), "w", encoding='utf-8')
arq.write('{"__class": "Tape","Clips":')
clips = '['

# Starts deserializing the mainsequence
if (JDVer == 2014):
    f.read(4) # Useless
    f.read(4) # Tape size (useless)
    f.read(8) # Header
    TapeNumber = struct.unpack('>I',f.read(4))[0] # Number of tapes
    for tape in range(TapeNumber):
        Class = f.read(8)
        
        # SoundSetClip deserialization
        if (Class == b'-\x8c\x88[\x00\x00\x00\x88'):
            print("SoundSetClip found!")
            f.read(12) # TrackId / Id / IsActive (Useless)
            serStartTime = struct.unpack('>I',f.read(4))[0] # Start Time
            serDuration = struct.unpack('>I',f.read(4))[0] # Duration
            f.read(4) # Empty bytes
            serPathLen = struct.unpack('>I',f.read(4))[0] # File path length
            FilePath = f.read(serPathLen).decode("utf-8") # File path
            serFileLen = struct.unpack('>I',f.read(4))[0] # File name length
            FileName = f.read(serFileLen).decode("utf-8") # Filename
            f.read(4) # ???
            if (TapeNumber > 1): # If it has more than one tape, it reads the separation bytes and go through it again
                f.read(12)
            else:
                pass
        
            # Writes SoundSetClip clips
            clips += '{"__class": "SoundSetClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": ' + str(serStartTime) + ',"Duration": ' + str(serDuration) + ',"SoundSetPath": "' + str(FilePath).replace('jd5', 'maps') + str(FileName) + '","SoundChannel": 0,"StartOffset": 0,"StopsOnEnd": 0,"AccountedForDuration": 0},'
        
        # TapeReferenceClip deserialization
        elif (Class == b'\x0E\x1E\x81\x58\x00\x00\x00\xA0'):
            print("TapeReferenceClip found!")
            f.read(12) # TrackId / Id / IsActive (Useless)
            serStartTime = struct.unpack('>I',f.read(4))[0] # Start Time
            serDuration = struct.unpack('>I',f.read(4))[0] # Duration
            serPathLen = struct.unpack('>I',f.read(4))[0] # File path length
            FilePath = f.read(serPathLen).decode("utf-8") # File path
            serFileLen = struct.unpack('>I',f.read(4))[0] # File name length
            FileName = f.read(serFileLen).decode("utf-8") # Filename
            f.read(4) # ???
            serLoop = struct.unpack('>I',f.read(4))[0] # Loop (PLACEHOLDER)
            if (TapeNumber > 1): # If it has more than one tape, it reads the separation bytes and go through it again
                f.read(12)
            else:
                pass
            
            # Writes TapeReferenceClip clips
            clips += '{"__class": "TapeReferenceClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": ' + str(serStartTime) + ',"Duration": ' + str(serDuration) + ',"Path": "' + str(FilePath).replace('jd5', 'maps') + str(FileName) + '","Loop": ' + str(serLoop) + '},'
        
        # AlphaClip deserialization
        elif (Class == b'\x86\x07\xd5\x82\x00\x00\x00@'):
            print("AlphaClip found!")
            f.read(12) # TrackId / Id / IsActive (Useless)
            serStartTime = struct.unpack('>I',f.read(4))[0] # Start Time
            serDuration = struct.unpack('>I',f.read(4))[0] # Duration
            serClips = struct.unpack('>I',f.read(4))[0] # Number of actor clips
            
            for numClips in range(serClips):
                if (numClips == 0):
                    aclips = '{"__class": "AlphaClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": ' + str(serStartTime) + ',"Duration": ' + str(serDuration) + ','
                else:
                    aclips += '{"__class": "AlphaClip", "Id": ' + str(randomId()) + ',"TrackId": ' + str(randomId()) + ',"IsActive": 1,"StartTime": ' + str(serStartTime) + ',"Duration": ' + str(serDuration) + ','
                if (numClips == 0):
                    f.read(4) # ???
                    serActorIndices = struct.unpack('>I',f.read(4))[0]
                    f.read(16) # ???
                
                for numActorIndices in range(serActorIndices):
                    serActor1 = struct.unpack('>I',f.read(4))[0] # Actor 1
                    Actor1 = f.read(serActor1).decode("utf-8") # Actor 1
                    f.read(8)
                    serActor2 = struct.unpack('>I',f.read(4))[0] # Actor 2
                    Actor2 = f.read(serActor2).decode("utf-8") # Actor 2
                    f.read(4)
                    serActor3 = struct.unpack('>I',f.read(4))[0] # Actor 3
                    Actor3 = f.read(serActor3).decode("utf-8") # Actor 3
                if (serClips > 1):
                    f.read(28) # ???
                aclips += '"ActorIndices": ["..|' + str(Actor1).lower() + '|' + str(Actor2).lower() + '|' + str(Actor3).lower() +'"],"Curve": {"__class": "BezierCurveFloat","Curve": { "__class": "BezierCurveFloatLinear", "ValueLeft": [' + str(float(0)) + ',' + str(float(0)) + '], "NormalLeftOut": ['+ str(float(0)) + ',' + str(float(0)) + '], "ValueRight": [' + str(float(0)) + ',' + str(float(0)) + '], "NormalRightIn": ['+ str(float(0)) + ',' + str(float(0)) + ']}}},'

            f.read(8)
            serValueLeft1 = struct.unpack('>I',f.read(4))[0]
            serValueLeft2 = struct.unpack('>I',f.read(4))[0]
            serNormalLeftOut1 = struct.unpack('>I',f.read(4))[0]
            serNormalLeftOut2 = struct.unpack('>I',f.read(4))[0]
            serValueRight1 = struct.unpack('>I',f.read(4))[0]
            serValueRight2 = struct.unpack('>I',f.read(4))[0]
            serNormalRightIn1 = struct.unpack('>I',f.read(4))[0]
            serNormalRightIn2 = struct.unpack('>I',f.read(4))[0]
            
            aclips = aclips.replace('"ValueLeft": [' + str(float(0)) + ',' + str(float(0)) + ']', '"ValueLeft": [' + str(float(serValueLeft1)) + ',' + str(float(serValueLeft2)) + ']')
            aclips = aclips.replace('"NormalLeftOut": [' + str(float(0)) + ',' + str(float(0)) + ']', '"NormalLeftOut": [' + str(float(serNormalLeftOut1)) + ',' + str(float(serNormalLeftOut2)) + ']')
            aclips = aclips.replace('"ValueRight": [' + str(float(0)) + ',' + str(float(0)) + ']', '"ValueRight": [' + str(float(serValueRight1)) + ',' + str(float(serValueRight2)) + ']')
            aclips = aclips.replace('"NormalRightIn": [' + str(float(0)) + ',' + str(float(0)) + ']', '"NormalRightIn": [' + str(float(serNormalRightIn1)) + ',' + str(float(serNormalRightIn2)) + ']')
            clips += aclips

# Writes the footer of the mainsequence
clips += '],"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": "' + os.path.basename(MainSequence).replace('_mainsequence.tape.ckd', '') +'","SoundwichEvent": ""}'
clips = clips.replace(',]', ']')
arq.write(clips)
arq.close()