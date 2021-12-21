import os
import sys
import json
import struct
from tkinter import *
from tkinter import filedialog
from dec_jd15 import dec_dtape
import pathlib

openFile = Tk()
openFile.title('')

# Gets DTAPE file
_temp_dtape_file = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu DTAPE", filetypes=[("DTAPE (.dtape.ckd)", "*.ckd")] )
_temp_codename = sys.argv[1]
_temp_output = sys.argv[2]

# Decrypts the DTAPE
dec_dtape(_temp_dtape_file, _temp_codename, _temp_output)