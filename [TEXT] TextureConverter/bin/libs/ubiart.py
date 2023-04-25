import os, sys, io, time, subprocess, struct, shutil
from bin.libs.texture import *

class Platform:
    def text2ubi(platform):
        # Create 'temp' folder
        Helpers.createFolder('temp')

        for PNGTexture in os.listdir("input"):
            match platform:
                case 'pc':
                    # Creates 'output/x360' folder
                    Helpers.createFolder('output/pc')

                    # Convert the file to DDS
                    Tools.texture2dds(PNGTexture)

                    # Convert the file to TGA.CKD
                    subprocess.check_call('"bin\\quickbms\\quickbms" -o "bin\\quickbms\\scriptDDStoCKD.bms" "temp\\' + PNGTexture.replace('.png', '.dds') + '" output\\pc\\', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                case 'wii':
                    print("Nintendo Wii texture system wasn't implemented yet...\nPlease wait for an update")
                    time.sleep(2)
                    break
                
                case 'wiiu':
                    # Creates 'output/wiiu' folder
                    Helpers.createFolder('output/wiiu')

                    # Convert the file to DDS
                    Tools.texture2dds(PNGTexture)
                    
                    # Converts the file to GTX
                    subprocess.run("bin\\texConv2\\TexConv2 -i \"temp\\" + PNGTexture.replace('.png', '.dds') + "\" -o \"temp\\" + PNGTexture.replace(".png", ".gtx") + "\"")
                    
                    # Converts the file to TGA.CKD
                    with open("temp\\" + PNGTexture.replace(".png", ".gtx"), "rb+") as f:
                        gtxdata = f.read()

                    ckdoutput = open("output\\wiiu\\" + PNGTexture.replace(".png", ".tga.ckd"), "wb+")
                    ckdoutput.write(b'\x00\x00\x00\x09\x54\x45\x58\x00\x00\x00\x00\x2C\x00\x00\x20\x80\x01\x00\x01\x00\x00\x01\x18\x00\x00\x00\x20\x80\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xCC\xCC')
                    ckdoutput.write(gtxdata)
                    ckdoutput.close()

                case 'ps3':
                    # Creates 'output/ps3' folder
                    Helpers.createFolder('output/ps3')
                    
                    # Convert the file to DDS
                    Tools.texture2dds(PNGTexture)

                    # Converts the file to GTF
                    subprocess.check_call('"bin\\dds2gtf" - temp\\' + PNGTexture.replace('.png', '.dds') + ' -o "temp/' + PNGTexture.replace('.png','.gtf') + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    # Converts the file to TGA.CKD
                    with open("temp/" + PNGTexture.replace(".png", ".gtf"), 'rb+') as f:
                        gtfdata = f.read()
                    ckdoutput=open("output/ps3/" + PNGTexture.replace('.png', '.tga.ckd'), 'wb+')
                    ckdoutput.write(b'\x00\x00\x00\x09\x54\x45\x58\x00\x00\x00\x00\x2C\x00\x02\xAB\x38\x04\x00\x04\x00\x00\x01\x18\x00\x00\x02\xAB\x38\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x02\x02\xCC\xCC')
                    ckdoutput.write(gtfdata)
                    ckdoutput.close()
                
                case 'x360':
                    # Creates 'output/x360' folder
                    Helpers.createFolder('output/x360')

                    # Converts the texture to TGA
                    Tools.texture2tga(PNGTexture)
                    
                    # Sets format type
                    if Helpers.getAlphaChannel(PNGTexture) == True:
                        dxtFMT = "D3DFMT_DXT5"
                    elif Helpers.getAlphaChannel(PNGTexture) == False:
                        dxtFMT = "D3DFMT_DXT1"

                    # Generate the RDF file (necessary to generate the XPR file)
                    Tools.rdfGenerator(PNGTexture, dxtFMT, Helpers.getTextureSize(PNGTexture)[0], Helpers.getTextureSize(PNGTexture)[1])
                    
                    # Converts the texture to XPR2
                    subprocess.check_call('"bin\\bundler.exe" "temp\\' + PNGTexture.replace('.png', '.rdf') + '" -o "temp/"' + PNGTexture.replace('.png', '.xpr') + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # Converts it onto a Xbox 360 TGA.CKD
                    with open('temp/' + PNGTexture.replace('.png', '.xpr'), "rb+") as XPR2File:

                        # Removes the XPR2 header
                        XPR2File.read(44)
                        IMGFile = XPR2File

                        # Writes everything onto the new TGA.CKD file
                        with open('output/x360/' + PNGTexture.replace('.png', '.tga') + ".ckd", "wb+") as CKDFile: # Creates the tga.ckd
                            
                            # Writes the X360 TGA.CKD header based if it's a transparent texture or not
                            X360Header = b'\x00\x00\x00\x09\x54\x45\x58\x00\x00\x00\x00\x2C'
                            X360Header += (os.path.getsize('temp/' + PNGTexture.replace('.png', '.xpr')) + 32).to_bytes(3, byteorder="big", signed=False)
                            X360Header += b'\x80\x02\x00\x02\x00\x00\x01\x20\x00'
                            X360Header += (os.path.getsize('temp/' + PNGTexture.replace('.png', '.xpr')) + 32).to_bytes(3, byteorder="big", signed=False)
                            X360Header += b'\x80\x00\x00\x00\x00\x00\x00\x71\x6A\x00\x03\x86\xD2\x02\x02\xCC\xCC'

                            # Writes the X360 TGA.CKD header alongside the XPR2 data
                            CKDFile.write(X360Header + XPR2File.read(52))
                            IMGFile.read(1964)
                            CKDFile.write(IMGFile.read())
                
                case 'nx':
                    # Creates 'output/nx' folder
                    Helpers.createFolder('output/nx')
                    
                    # Convert the file to DDS
                    Tools.texture2dds(PNGTexture)

                    # Convert the texture to XTX
                    subprocess.check_call('"bin\\xtx_extract\\xtx_extract" -o "temp\\' + PNGTexture.replace(".png",".xtx") + '" "temp\\' + PNGTexture.replace('.png', '.dds') + '"', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    # Convert the texture to TGA.CKD
                    ckdoutput = open("output/nx/"+ PNGTexture.replace(".png", ".tga.ckd"), "wb+")
                    ckdoutput.write(b'\x00\x00\x00\x09\x54\x45\x58\x00\x00\x00\x00\x2C\x00\x00\x20\x80\x01\x00\x01\x00\x00\x01\x18\x00\x00\x00\x20\x80\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xCC\xCC')
                    with open("temp/" + PNGTexture.replace(".png", ".xtx"), "rb+") as f:
                        xtxdata = f.read()
                    ckdoutput.write(xtxdata)
                    ckdoutput.close()

        # Clean 'temp' folder
        shutil.rmtree('temp')
    
    def ubi2text(platform):
        print("nope")