import os, sys, io, time, pathlib, subprocess, shutil
from tkinter import *
from tkinter import filedialog

# Creates "output" directory 
os.makedirs('output', exist_ok=True)

def PCWEBMConv():
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
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + (videofolder + "/" + videofile).replace("/", "\\") + '" -threads:v 4 -sws_flags bicubic -codec:v libvpx  -r:v 25  -b:v 8000k -bufsize 6000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -b:v 7000k  -aspect 16:9 -b:v 8000k -filter:v scale=1280:720 "output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call('"bin\\mkclean.exe" "output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '" "output\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Cleans unnecessary stuff
            print("Cleaning files...\n")
            os.remove('output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))
            os.rename('output\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"), 'output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))
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
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + videofile + '" -threads:v 4 -sws_flags bicubic -codec:v libvpx  -r:v 25  -b:v 8000k -bufsize 6000k -g 120 -rc_lookahead 16 -profile:v 1 -qmax 51 -qmin 11 -slices 4 -quality realtime -an -vol 0 -b:v 7000k  -aspect 16:9 -b:v 8000k -filter:v scale=1280:720 "output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call('"bin\\mkclean.exe" "output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '" "output\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleans unnecessary stuff
        print("Cleaning files...\n")
        os.remove('output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))
        os.rename('output\\clean.' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"), 'output\\' + os.path.basename(videofile).replace(os.path.basename(videofile).split(".")[-1], "webm"))

def PCWAVConv():
    if (BatchQ == "Y" or BatchQ == "y"):
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary folder
        audiofolder = filedialog.askdirectory(initialdir=str(pathlib.Path().absolute()), title="Select your video / audio folder")
        
        # Destroys Tkinter
        openFile.destroy()
        
        # For each file found inside the desired folder...
        for audiofile in os.listdir(audiofolder):
            # Converts the video into a WAV (for the WAV.CKD generator)
            print("Converting " + os.path.basename(audiofile) + " to PC WAV.CKD...")
            subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + (audiofolder + "/" + audiofile).replace("/", "\\") + '" -ac 2 -f wav "output\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Converts the WAV onto a WAV.CKD
            with open('output\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"), "rb+") as wav:
                wav.read(20) # Takes the wav header
                ckdheader = b'\x52\x41\x4B\x49\x0A\x00\x00\x00\x4D\x49\x58\x20\x70\x63\x6D\x20\xB2\x1E\x00\x00\xB8\x1E\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x66\x6D\x74\x20\x50\x00\x00\x00\x10\x00\x00\x00\x4D\x41\x52\x4B\x60\x00\x00\x00\xC8\x08\x00\x00\x53\x54\x52\x47\x28\x09\x00\x00\x8A\x15\x00\x00\x64\x61\x74\x61\xB8\x1E\x00\x00\x04\x86\x95\x02' # Writes the PC RAKI Header
               
                # Writes everything onto the new WAV.CKD file
                with open("output//" + os.path.basename(audiofile) + ".ckd", "wb+") as ckd: # Creates the wav.ckd
                    ckd.write(ckdheader + wav.read())# Writes the PC HAKI header alongside the WAV data
            
            # Cleans unnecessary stuff
            print("Cleaning files...\n")
            os.remove('output\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"))
    else:
        # Initializes Tkinter (file picker)
        openFile = Tk()
        openFile.title('')
        
        # Searches for the necessary file
        audiofile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your video / audio file", filetypes=[("Video / Audio (.mp4 / .bik / .webm / .avi / .mkv / .mov / .wav / .ogg / .mp3 / .m4a)", "*.mp4 *.bik *.webm *.avi *.mkv *.mov *.wav *.ogg *.mp3 *.m4a")])
        
        # Destroys Tkinter
        openFile.destroy()
        
        # Converts the video into a WAV (for the WAV.CKD generator)
        print("Converting " + os.path.basename(audiofile) + " to PC WAV.CKD...")
        subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + audiofile + '" -ar 48000 -ac 2 -f wav "output\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Converts the WAV onto a WAV.CKD
        with open('output\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"), "rb+") as wav:
            wav.read(20) # Takes the wav header
            ckdheader = b'\x52\x41\x4B\x49\x0A\x00\x00\x00\x4D\x49\x58\x20\x70\x63\x6D\x20\xB2\x1E\x00\x00\xB8\x1E\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x66\x6D\x74\x20\x50\x00\x00\x00\x10\x00\x00\x00\x4D\x41\x52\x4B\x60\x00\x00\x00\xC8\x08\x00\x00\x53\x54\x52\x47\x28\x09\x00\x00\x8A\x15\x00\x00\x64\x61\x74\x61\xB8\x1E\x00\x00\x04\x86\x95\x02' # Writes the PC RAKI Header
           
            # Writes everything onto the new WAV.CKD file
            with open("output//" + os.path.basename(audiofile) + ".ckd", "wb+") as ckd: # Creates the wav.ckd
                ckd.write(ckdheader + wav.read())# Writes the PC HAKI header alongside the WAV data
        
        # Cleans unnecessary stuff
        print("Cleaning files...\n")
        os.remove('output\\' + os.path.basename(audiofile).replace(os.path.basename(audiofile).split(".")[-1], "wav"))
        
def PCAMBConv():
    # Initializes Tkinter (file picker)
    openFile = Tk()
    openFile.title('')
    
    # Searches for the necessary file
    ambfile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your No HUD video", filetypes=[("Audio (.wav / .ogg / .mp3 / .m4a)", "*.wav *.ogg *.mp3 *.m4a")])
    
    # Destroys Tkinter
    openFile.destroy()
    
    # Converts AMB audio onto a Little Endian 16-bit PCM audio
    subprocess.check_call('"bin\\ffmpeg.exe" -y -i "' + ambfile + '" -f wav -bitexact -acodec pcm_s16le -ar 48000 -ac 2 -loglevel quiet "output\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav") + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Creates "ambs" directory inside of "output"
    os.makedirs('output\\ambs', exist_ok=True)
    
    # Converts the new 16-bit PCM audio to WAV.CKD
    with open('output\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav"), 'rb+') as wav:
        
        # Replaces WAV header with empty bytes (instead of cropping it) (It fixes the popping sound at the beginning of the AMB)
        wav.read(43)
        
        # Writes the NX RAKI header (as NX AMBs work on PC, it should be fine)
        rakiheader = b'\x52\x41\x4B\x49\x0B\x00\x00\x00\x4E\x78\x20\x20\x70\x63\x6D\x20\x48\x00\x00\x00\x48\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x66\x6D\x74\x20\x38\x00\x00\x00\x10\x00\x00\x00\x64\x61\x74\x61\x48\x00\x00\x00' # Writes the start of the NX RAKI header
        rakiheader += (os.path.getsize('output\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav")) - 72).to_bytes(3, byteorder="little", signed=False) # Takes the file size, reduces it by 72 and then writes it to the file (3 bytes)
        rakiheader += b'\x00\x01\x00\x02\x00\x80\xBB\x00\x00\x00\xEE\x02\x00\x04\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00' # Writes the end of the NX RAKI header
        
        # Writes everything onto the new WAV.CKD file
        with open('output\\ambs\\'+ os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav") + '.ckd', 'wb+') as wavckd:
            wavckd.write(rakiheader + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + wav.read())
            wavckd.close()
            wav.close()
            
    # Deletes the 16-bit PCM WAV audio file
    os.remove('output\\' + os.path.basename(ambfile).replace(os.path.basename(ambfile).split(".")[-1], "wav"))
    
if __name__=='__main__':
    while(True):
        os.system('cls')
        print("How're you doing?")
        print("Welcome to WodsonKun's MediaTool!")
        print("Credits to: Eliott")
        print("Select a option:")
        print("-----------------------------")
        print('[1] Converts a Video file to PC WEBM')
        print('[2] Converts a Video / Audio file to PC WAV.CKD')
        print('[3] Converts a Audio file to PC AMB')
        print('[4] Exits the MediaTool')
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
            print('Thanks for using our MediaTool!')
            time.sleep(2)
            exit()
        
        else:
            print('Wrong option! Please, choose a valid option')