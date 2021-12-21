import os
import sys
import json
import struct
from tkinter import *
from tkinter import filedialog
from dec_jd14 import dec_sd_14
import pathlib

openFile = Tk()
openFile.title('')

# Gets timeline file
_temp_sd_file = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione sua songdesc", filetypes=[("Songdesc (.tml.ckd)", "*.ckd")] )
_temp_codename = sys.argv[1]
_temp_output = sys.argv[2]

# Decrypts the timeline
dec_sd_14(_temp_sd_file, _temp_codename, _temp_output)