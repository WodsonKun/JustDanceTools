import os
import sys
import json
import struct
from tkinter import *
from tkinter import filedialog
from dec_jd15 import dec_ktape
import pathlib

openFile = Tk()
openFile.title('')

# Gets KTAPE file
_temp_ktape_file = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu KTAPE", filetypes=[("KTAPE (.ktape.ckd)", "*.ckd")] )
_temp_codename = sys.argv[1]
_temp_output = sys.argv[2]

# Decrypts the KTAPE
dec_ktape(_temp_ktape_file, _temp_codename, _temp_output)