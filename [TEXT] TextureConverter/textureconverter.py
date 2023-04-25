import os, sys, io
from bin.libs.ubiart import *

# WodsonKun's TextureConverter
if __name__=='__main__':
    while(True):
        os.system('cls')
        print("How're you doing?")
        print("Welcome to WodsonKun's TextureConverter!")
        print("Select a option:")
        print("-----------------------------")
        print("[1] Convert textures to PC format")
        print("[2] Convert textures to Wii format")
        print("[3] Convert textures to Wii U format")
        print("[4] Convert textures to Xbox 360 format")
        print("[5] Convert textures to PlayStation 3 format")
        print("[6] Convert textures to Nintendo Switch format")
        print("[7] Exits the TextureConverter")
        print("-----------------------------")
        
        option = ''
        try:
            option = int(input('Choose your option: '))
        except:
            print('')
        
        #Check what choice was entered and act accordingly
        if option == 1:
            Platform.text2ubi('pc')
        if option == 2:
            Platform.text2ubi('wii')
        if option == 3:
            Platform.text2ubi('wiiu')
        if option == 4:
            Platform.text2ubi('x360')
        if option == 5:
            Platform.text2ubi('ps3')
        if option == 6:
            Platform.text2ubi('nx')
        if option == 7:
            print('Thanks for using our TextureConverter!')
            exit()
        else:
            print('Wrong option! Please, choose a valid option')