def PictoCutter(CodeName, CoachCount, outputfolder, stretch=True):
    import requests
    from PIL import Image
    from io import BytesIO
    CoachCount = int(CoachCount)
    css = requests.get("http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/songs/" + CodeName + "/assets/web/pictos-sprite.css").text.split("\n")
    pictoAtlas = Image.open(BytesIO(requests.get("http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/songs/" + CodeName + "/assets/web/pictos-sprite.png", stream=True).content))
    if CoachCount > 1:
        y1 = 40
        x1 = 217
    else:
        y1 = 0
        x1 = 256
    x = 256
    y = 0
    for picto in css:
        pictoName = picto.split("-")[1].split("{")[0]
        picto = pictoAtlas.crop((y,y1,x,x1))
        y = y + 256
        x = x + 256
        if (CoachCount > 1) and stretch:
            picto = picto.resize((256,256))
        picto.save(outputfolder + pictoName + ".png")
