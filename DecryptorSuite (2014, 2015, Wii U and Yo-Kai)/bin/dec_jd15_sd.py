import os
import sys
import json
import struct
from tkinter import *
from tkinter import filedialog
from dec_jd15 import dec_sd_15
import pathlib

openFile = Tk()
openFile.title('')

# Gets songdesc file
_temp_sd_file = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione seu songdesc", filetypes=[("Songdesc (.tpl.ckd)", "*.ckd")] )
_temp_codename = sys.argv[1]
_temp_output = sys.argv[2]

# Decrypts the songdesc
dec_sd_15(_temp_sd_file, 0, _temp_codename, _temp_output)