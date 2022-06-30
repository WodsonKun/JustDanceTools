import os, sys, io, json, time, pathlib, subprocess, shutil
from tkinter import *
from tkinter import filedialog

# Creates "output" directory 
os.makedirs('output', exist_ok=True)

def PCWEBMConv():
    # Creates "output" directory 
    os.makedirs('output\\pc', exist_ok=True)
    
    if (BatchQ == "Y" or BatchQ == "y"):
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary folder
        videofolder = filedialog.askdirectory(initialdir=str(pathlib.Path().absolute()), title="Select your No HUDs folder")
        
        # Destroys Tkinter
        openFile.destroy()
        
        # For each file found inside the desired folder...
        for videofile in os.listdir(videofolder):
            # Converts and cleans the No HUD
            print("Converting " + os.path.basename(videofile) + " to PC WEBM...")
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + (videofolder + "/" + videofile).replace("/", "\\") + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 8000k -bufsize 8000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 5:3 -filter:v scale=1216:720 "output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '" "output\\pc\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Cleans unnecessary stuff
            print("Cleaning files...\n")
            os.remove('output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))
            os.rename('output\\pc\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))
    else:
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary file
        videofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video file", filetypes=[("Video (.mp4 / .bik / .webm / .avi / .mkv / .mov)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov")])
        
        # Destroys Tkinter
        openFile.destroy()
        
        # Converts and cleans the No HUD
        print("Converting " + os.path.basename(videofile) + " to PC WEBM...")
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 8000k -bufsize 8000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 5:3 -filter:v scale=1216:720 "output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '" "output\\pc\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleans unnecessary stuff
        print("Cleaning files...\n")
        os.remove('output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))
        os.rename('output\\pc\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))

def PCWAVConv():
    # Creates "output" directory 
    os.makedirs('output\\pc', exist_ok=True)
    
    if (BatchQ == "Y" or BatchQ == "y"):
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary folder
        audiofolder = filedialog.askdirectory(initialdir=str(pathlib.Path().absolute()), title="Select your video / audio folder")
        
        # Destroys Tkinter
        openFile.destroy()
        
        # Volume?
        QVolume = str(input("Do you wanna increase the volume? (Useful for JDU / JDN OGGs and MP4s) (Y or N)): "))
        
        # For each file found inside the desired folder...
        for audiofile in os.listdir(audiofolder):
            # Converts the video into a WAV (for the WAV.CKD generator)
            print("Converting " + os.path.basename(audiofile) + " to PC WAV.CKD...")
            if (QVolume == "Y" or QVolume == "y"):
                subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + (audiofolder + "/" + audiofile).replace("/", "\\") + '" -ar 48000 -ac 2 -filter:a "volume=12dB" -f wav "output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + (audiofolder + "/" + audiofile).replace("/", "\\") + '" -ar 48000 -ac 2 -f wav "output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Converts the WAV onto a WAV.CKD
            with open('output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"), "rb+") as wav:
                wav.read(20) # Takes the wav header
                ckdheader = b'\x52\x41\x4B\x49\x0A\x00\x00\x00\x4D\x49\x58\x20\x70\x63\x6D\x20\xB2\x1E\x00\x00\xB8\x1E\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x66\x6D\x74\x20\x50\x00\x00\x00\x10\x00\x00\x00\x4D\x41\x52\x4B\x60\x00\x00\x00\xC8\x08\x00\x00\x53\x54\x52\x47\x28\x09\x00\x00\x8A\x15\x00\x00\x64\x61\x74\x61\xB8\x1E\x00\x00\x04\x86\x95\x02' # Writes the PC RAKI Header
               
                # Writes everything onto the new WAV.CKD file
                with open("output\\pc\\" + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + ".ckd", "wb+") as ckd: # Creates the wav.ckd
                    ckd.write(ckdheader + wav.read())# Writes the PC HAKI header alongside the WAV data
            
            # Cleans unnecessary stuff
            print("Cleaning files...\n")
            os.remove('output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"))
    else:
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary file
        audiofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video / audio file", filetypes=[("Video / Audio (.mp4 / .bik / .webm / .avi / .mkv / .mov / .wav / .ogg / .mp3 / .m4a)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov *.wav *.ogg *.mp3 *.m4a")])
        
        # Destroys Tkinter
        openFile.destroy()
        
        # Volume?
        QVolume = str(input("Do you wanna increase the volume? (Useful for JDU / JDN OGGs and MP4s) (Y or N)): "))
        
        # Converts the video into a WAV (for the WAV.CKD generator)
        print("Converting " + os.path.basename(audiofile) + " to PC WAV.CKD...")
        if (QVolume == "Y" or QVolume == "y"):
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + audiofile + '" -ar 48000 -ac 2 -filter:a "volume=12dB" -f wav "output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + audiofile + '" -ar 48000 -ac 2 -f wav "output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Converts the WAV onto a WAV.CKD
        with open('output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"), "rb+") as wav:
            wav.read(20) # Takes the wav header
            ckdheader = b'\x52\x41\x4B\x49\x0A\x00\x00\x00\x4D\x49\x58\x20\x70\x63\x6D\x20\xB2\x1E\x00\x00\xB8\x1E\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x66\x6D\x74\x20\x50\x00\x00\x00\x10\x00\x00\x00\x4D\x41\x52\x4B\x60\x00\x00\x00\xC8\x08\x00\x00\x53\x54\x52\x47\x28\x09\x00\x00\x8A\x15\x00\x00\x64\x61\x74\x61\xB8\x1E\x00\x00\x04\x86\x95\x02' # Writes the PC RAKI Header
           
            # Writes everything onto the new WAV.CKD file
            with open("output\\pc\\" + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + ".ckd", "wb+") as ckd: # Creates the wav.ckd
                ckd.write(ckdheader + wav.read())# Writes the PC HAKI header alongside the WAV data
        
        # Cleans unnecessary stuff
        print("Cleaning files...\n")
        os.remove('output\\pc\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"))
        
def PCAMBConv():
    # Initializes Tkinter (file picker)
    openFile = Tk()
    openFile.title('')
    
    # Searches for the necessary file
    ambfile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your No HUD video", filetypes=[("Audio (.wav / .ogg / .mp3 / .m4a)", "*.wav *.ogg *.mp3 *.m4a")])
    
    # Destroys Tkinter
    openFile.destroy()
    
    # Volume?
    QVolume = str(input("Do you wanna increase the volume? (Useful for JDU / JDN OGGs and MP4s) (Y or N)): "))
    
    # Converts AMB audio onto a Little Endian 16-bit PCM audio
    print("Converting " + os.path.basename(ambfile) + " to PC AMB...")
    if (QVolume == "Y" or QVolume == "y"):
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + ambfile + '" -f wav -bitexact -acodec pcm_s16le -filter:a "volume=12dB" -ar 48000 -ac 2 -loglevel quiet "output\\pc\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + ambfile + '" -f wav -bitexact -acodec pcm_s16le -ar 48000 -ac 2 -loglevel quiet "output\\pc\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Creates "ambs" directory inside of "output"
    os.makedirs('output\\pc\\ambs', exist_ok=True)
    
    # Converts the new 16-bit PCM audio to WAV.CKD
    with open('output\\pc\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav"), 'rb+') as wav:
        
        # Replaces WAV header with empty bytes (instead of cropping it) (It fixes the popping sound at the beginning of the AMB)
        wav.read(43)
        
        # Writes the NX RAKI header (as NX AMBs work on PC, it should be fine)
        rakiheader = b'\x52\x41\x4B\x49\x0B\x00\x00\x00\x4E\x78\x20\x20\x70\x63\x6D\x20\x48\x00\x00\x00\x48\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x66\x6D\x74\x20\x38\x00\x00\x00\x10\x00\x00\x00\x64\x61\x74\x61\x48\x00\x00\x00' # Writes the start of the NX RAKI header
        rakiheader += (os.path.getsize('output\\pc\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav")) - 72).to_bytes(3, byteorder="little", signed=False) # Takes the file size, reduces it by 72 and then writes it to the file (3 bytes)
        rakiheader += b'\x00\x01\x00\x02\x00\x80\xBB\x00\x00\x00\xEE\x02\x00\x04\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00' # Writes the end of the NX RAKI header
        
        # Writes everything onto the new WAV.CKD file
        with open('output\\pc\\ambs\\'+ os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav") + '.ckd', 'wb+') as wavckd:
            wavckd.write(rakiheader + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + wav.read())
            wavckd.close()
            wav.close()
            
    # Deletes the 16-bit PCM WAV audio file
    os.remove('output\\pc\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav"))

def WiiWEBMConv():
    if (BatchQ == "Y" or BatchQ == "y"):
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary folder
        videofolder = filedialog.askdirectory(initialdir=str(pathlib.Path().absolute()), title="Select your No HUDs folder")
        
        # Destroys Tkinter
        openFile.destroy()
        
        # For each file found inside the desired folder...
        for videofile in os.listdir(videofolder):
            # Converts and cleans the No HUD
            print("Converting " + os.path.basename(videofile) + " to Wii WEBM...")
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + (videofolder + "/" + videofile).replace("/", "\\") + '" -threads:v 3 -sws_flags bicubic -codec:v libvpx -r:v 25 -b:v 2200k -bufsize 2200k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -an -vol 0 -aspect 4:3 -filter:v scale=512:384 "output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call('"bin\\mkclean.exe" "output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm") + '" "output\\wii\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Cleans unnecessary stuff
            print("Cleaning files...\n")
            os.remove('output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm"))
            os.rename('output\\wii\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm"), 'output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm"))
    else:
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary file
        videofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video file", filetypes=[("Video (.mp4 / .bik / .webm / .avi / .mkv / .mov)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov")])
        
        # Destroys Tkinter
        openFile.destroy()
        
        # Converts and cleans the No HUD
        print("Converting " + os.path.basename(videofile) + " to Wii WEBM...")
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -codec:v libvpx -r:v 25 -b:v 2200k -bufsize 2200k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -an -vol 0 -aspect 4:3 -filter:v scale=512:384 "output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" "output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm") + '" "output\\wii\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleans unnecessary stuff
        print("Cleaning files...\n")
        os.remove('output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm"))
        os.rename('output\\wii\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm"), 'output\\wii\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "wii.webm"))
        
def WiiWAVConv():
    # Initializes Tkinter (file picker)
    openFile = Tk()
    openFile.title('')
    
    # Searches for the necessary file
    audiofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video file", filetypes=[("Video / Audio (.mp4 / .bik / .webm / .avi / .mkv / .mov / .wav / .ogg / .mp3 / .m4a)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov *.wav *.ogg *.mp3 *.m4a")])
    
    # Destroys Tkinter
    openFile.destroy()
    
    # Creates a 'temp' folder
    os.makedirs("output//temp", exist_ok=True)
    
    # Starts converting the audio / amb
    print("Converting " + os.path.basename(audiofile) + " to Wii WAV.CKD...")
    if ('.mp4' in audiofile):
        subprocess.check_call('bin//ffmpeg.exe -y -i ' + audiofile + ' -ar 32000 -filter:a "volume=12dB" -map_channel 0.1.0 "output//temp//left.wav" -ar 32000 -filter:a "volume=12dB" -map_channel 0.1.1 "output//temp//right.wav"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.check_call('bin//ffmpeg.exe -y -i ' + audiofile + ' -ar 32000 -map_channel 0.0.0 "output//temp//left.wav" -ar 32000 -map_channel 0.0.1 "output//temp//right.wav"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Transforms the divided audio in DSP
    subprocess.check_call('bin//VGAudioCli.exe "output//temp//left.wav" "output//temp//left.dsp"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.check_call('bin//VGAudioCli.exe "output//temp//right.wav" "output//temp//right.dsp"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # ?
    rightbytes = []
    leftbytes = []
    filesize = (os.path.getsize("output//temp//left.dsp") - 96)
    leftcoefs = b''
    rightcoefs = b''
    
    # ??
    with open("output//temp//left.dsp", "rb") as f:
        leftcoefs = f.read(96)
        for i in range(int(filesize/8)): 
            byte = f.read(8)
            leftbytes.append(byte)

    with open("output//temp//right.dsp", "rb") as f:
        rightcoefs = f.read(96)
        for i in range(int(filesize/8)): 
            byte = f.read(8)
            rightbytes.append(byte)
            
    # Clean useless files
    os.remove("output//temp//left.wav")
    os.remove("output//temp//right.wav")
    os.remove("output//temp//left.dsp")
    os.remove("output//temp//right.dsp")
    os.rmdir("output//temp")
    
    # Writes the new WAV.CKD/AMB file
    offsetinfo = 320
    denc = open("output\\wii\\" + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + ".ckd", "wb")
    denc.write(b'\x52\x41\x4B\x49\x00\x00\x00\x09\x57\x69\x69\x20\x61\x64\x70\x63\x00\x00\x01\x2E\x00\x00\x01\x40\x00\x00\x00\x05\x00\x00\x00\x00\x66\x6D\x74\x20\x00\x00\x00\x5C\x00\x00\x00\x12\x64\x73\x70\x4C\x00\x00\x00\x6E\x00\x00\x00\x60\x64\x73\x70\x52\x00\x00\x00\xCE\x00\x00\x00\x60\x64\x61\x74\x4C\x00\x00\x01\x40')
    denc.write((len(leftbytes)*8).to_bytes(4, 'big'))
    denc.write(b'\x64\x61\x74\x52')
    denc.write((offsetinfo + (len(leftbytes)*8)).to_bytes(4, 'big'))
    denc.write((len(rightbytes)*8).to_bytes(4, 'big'))
    denc.write(b'\x00\x02\x00\x02\x00\x00\x7D\x00\x00\x00\xFA\x00\x00\x02\x00\x10\x00\x00')
    denc.write(leftcoefs)
    denc.write(rightcoefs)
    denc.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    for i in range(int(filesize/8)):
        denc.write(leftbytes[i])
    for i in range(int(filesize/8)):
        denc.write(rightbytes[i])   
    denc.close()

def JDUWEBMConv():
    # Initializes Tkinter (file picker)
    openFile = Tk()
    openFile.title('')
    
    # Searches for the necessary file
    videofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video file", filetypes=[("Video (.mp4 / .bik / .webm / .avi / .mkv / .mov)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov")])
    
    # Destroys Tkinter
    openFile.destroy()
    
    # Asks if you wanna convert to HD format too
    qHDWEBM = str(input('Do you wanna convert them to HD too (PS4 / XB1)? (Y or N):'))
    
    # Converts and cleans the No HUD
    print("Converting " + os.path.basename(videofile) + " to JDU WEBMs...")
    if (qHDWEBM == "Y" or qHDWEBM == 'y'):
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 600k -bufsize 600k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=480:270 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 700k -bufsize 700k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=480:270 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 800k -bufsize 800k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=768:432 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 900k -bufsize 900k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=768:432 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 2000k -bufsize 2000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=1280:720 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 3000k -bufsize 3000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=1216:720 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 6000k -bufsize 6000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 5:3 -filter:v scale=1216:720 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 8000k -bufsize 8000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=1920:1080 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.hd.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.hd.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.hd.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.hd.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.hd.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 600k -bufsize 600k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=480:270 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 800k -bufsize 800k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=768:432 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 2000k -bufsize 2000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 16:9 -filter:v scale=1280:720 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 3 -sws_flags bicubic -c:v libvpx -r:v 25 -b:v 6000k -bufsize 6000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -aspect 5:3 -filter:v scale=1216:720 "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" --doctype 2 --optimize "output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm") + '" "output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Cleans unnecessary stuff
    print("Cleaning files...\n")
    if (qHDWEBM == "Y" or qHDWEBM == 'y'):
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.hd.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.hd.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.hd.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.hd.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.hd.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.hd.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.hd.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.hd.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.hd.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.hd.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.hd.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.hd.webm"))
    else:
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm"))
        os.remove('output\\jdu\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_LOW.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_MID.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_HIGH.webm"))
        os.rename('output\\jdu\\clean.' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm"), 'output\\pc\\' + os.path.basename(videofile).replace(os.path.splitext(videofile)[1], "_ULTRA.webm"))

def JDUOGGConv():
    # Initializes Tkinter (file picker)
    openFile = Tk()
    openFile.title('')
    
    # Searches for the necessary file
    audiofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video / audio file", filetypes=[("Video / Audio (.mp4 / .bik / .webm / .avi / .mkv / .mov / .wav / .ogg / .mp3 / .m4a)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov *.wav *.ogg *.mp3 *.m4a")])
    
    # Destroys Tkinter
    openFile.destroy()
    
    # Converts the video into a OGG
    subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + audiofile + '" -ar 48000 -vn -c:a libvorbis "output\\jdu\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "ogg") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
if __name__=='__main__':
    while(True):
        os.system('cls')
        print("How're you doing?")
        print("Welcome to WodsonKun's MediaTool!")
        print("Credits to: Eliott, augustodoidin")
        print("Select a option:")
        print("-----------------------------")
        print('[1] Converts a video file to PC WEBM')
        print('[2] Converts a video / audio file to PC WAV.CKD')
        print('[3] Converts a audio file to PC AMB')
        print('[4] Converts a video file to Nintendo Wii WEBM')
        print('[5] Converts a video / audio file to Nintendo Wii WAV.CKD / AMB')
        print('[6] Converts a video file to Just Dance Unlimited WEBMs')
        print('[7] Converts a video / audio file to Just Dance Unlimited OGG')
        print('[8] Exits the MediaTool')
        print("-----------------------------")
        
        option = ''
        try:
            option = int(input('Choose your option: '))
        except:
            print('')
        
        #Check what choice was entered and act accordingly
        if option == 1:
            BatchQ = str(input("Do you wanna batch convert? (Y or N): "))
            PCWEBMConv()
        
        if option == 2:
            BatchQ = str(input("Do you wanna batch convert? (Y or N): "))
            PCWAVConv()
        
        if option == 3:
            PCAMBConv()
            
        if option == 4:
            BatchQ = str(input("Do you wanna batch convert? (Y or N): "))
            WiiWEBMConv()
        
        if option == 5:
            WiiWAVConv()
            
        if option == 6:
            JDUWEBMConv()
            
        if option == 7:
            JDUOGGConv()
        
        if option == 8:
            print('Thanks for using our MediaTool!')
            time.sleep(2)
            exit()
        
        else:
            print('Wrong option! Please, choose a valid option')