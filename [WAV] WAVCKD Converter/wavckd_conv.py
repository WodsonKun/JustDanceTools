import os, sys, io, pathlib
from tkinter import *
from tkinter import filedialog

# Cria uma pasta output
os.makedirs("output", exist_ok=True)

# Inicializa o Tkinter (para usar o seletor de arquivos)
openFile = Tk()
openFile.title('')

# Procura o JSON principal (apenas ele é usado para gerar a songdesc)
wavfile = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select your WAV file", filetypes=[("WAV (.wav)", "*.wav")] )
    
# Destrói o Tkinter (poupa memória e tira a janelinha que fica atrapalhando)
openFile.destroy()

# Converte para WAV.CKD
with open(wavfile, "rb+") as wav:
    wav.read(20)##It takes the wav header
    ckdheader = b'\x52\x41\x4B\x49\x0A\x00\x00\x00\x4D\x49\x58\x20\x70\x63\x6D\x20\xB2\x1E\x00\x00\xB8\x1E\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x66\x6D\x74\x20\x50\x00\x00\x00\x10\x00\x00\x00\x4D\x41\x52\x4B\x60\x00\x00\x00\xC8\x08\x00\x00\x53\x54\x52\x47\x28\x09\x00\x00\x8A\x15\x00\x00\x64\x61\x74\x61\xB8\x1E\x00\x00\x04\x86\x95\x02'
    with open("output//" + os.path.basename(wavfile) + ".ckd", "wb+") as ckd:##It creates the wav.ckd
        ckd.write(ckdheader)##Writes the ckd header
        ckd.write(wav.read())##Writes the wav