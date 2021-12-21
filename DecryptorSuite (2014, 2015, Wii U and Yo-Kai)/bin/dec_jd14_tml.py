import os
import sys
import json
import struct
from tkinter import *
from tkinter import filedialog
from dec_jd14 import dec_tml
import pathlib

openFile = Tk()
openFile.title('')

# Gets timeline file
_temp_tml_file = openFile.filename = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Selecione sua timeline", filetypes=[("Timeline (.tml.ckd)", "*.ckd")] )
_temp_codename = sys.argv[1]
_temp_output = sys.argv[2]

# Decrypts the timeline
dec_tml(_temp_tml_file, _temp_codename, _temp_output)