# SongDB Generator
# Prompts
CodeName = input("Codename: ")
Title = input("Song title: ")
Artist = input("Song artist: ")
BPM = int(input("Song BPM: "))
startBeat = int(input("startBeat (check MusicTrack): "))
endBeat = int(input("endBeat (check MusicTrack): "))
CoachCount = int(input("Coach count: "))
LocaleID = input("It's a Alternate / VIPMADE / CMU / MU / Etc.? (yes or no): ")
LyricsColor = input("Lyrics color (in hex): ")
Difficulty = input("Difficulty: ")
LyricsType = int(input("Lyrics type (0 = Normal, 3 = On Stage): "))
OriginalJDVersion = int(input("Original JD game: "))

# SongDB
arq = open(CodeName.lower() + "_songdb.json", "w")
arq.write('{')
arq.write('"' + CodeName + '": {')
arq.write('"artist": "' + Artist + '",')
arq.write('"assets": {')
arq.write('"banner_bkgImageUrl": "",')
if (CoachCount == 1):
    arq.write('"coach1ImageUrl": "",')
if (CoachCount == 2):
    arq.write('"coach1ImageUrl": "",')
    arq.write('"coach2ImageUrl": "",')
if (CoachCount == 3):
    arq.write('"coach1ImageUrl": "",')
    arq.write('"coach2ImageUrl": "",')
    arq.write('"coach3ImageUrl": "",')
if (CoachCount == 4):
    arq.write('"coach1ImageUrl": "",')
    arq.write('"coach2ImageUrl": "",')
    arq.write('"coach3ImageUrl": "",')
    arq.write('"coach4ImageUrl": "",')
arq.write('"coverImageUrl": "",')
arq.write('"cover_1024ImageUrl": "",')
arq.write('"cover_smallImageUrl": "",')
arq.write('"expandBkgImageUrl": "",')
arq.write('"expandCoachImageUrl": "",')
if (CoachCount == 1):
    arq.write('"phoneCoach1ImageUrl": "",')
if (CoachCount == 2):
    arq.write('"phoneCoach1ImageUrl": "",')
    arq.write('"phoneCoach2ImageUrl": "",')
if (CoachCount == 3):
    arq.write('"phoneCoach1ImageUrl": "",')
    arq.write('"phoneCoach2ImageUrl": "",')
    arq.write('"phoneCoach3ImageUrl": "",')
if (CoachCount == 4):
    arq.write('"phoneCoach1ImageUrl": "",')
    arq.write('"phoneCoach2ImageUrl": "",')
    arq.write('"phoneCoach3ImageUrl": "",')
    arq.write('"phoneCoach4ImageUrl": "",')
arq.write('"phoneCoverImageUrl": "",')
arq.write('"map_bkgImageUrl": ""')
arq.write('},')
arq.write('"audioPreviewData": "{\\"__class\\":\\"MusicTrackData\\",\\"structure\\":{\\"__class\\":\\"MusicTrackStructure\\",\\"markers\\":[')

# Augusto's Beat Generator (used to... generate beats?)
beat = int(round(60000/BPM))
MSFinal = 30000
gerados = 0
beatatual = 0
while(beatatual <= MSFinal):
    if(beat*gerados < MSFinal and beat*(gerados+1) >= MSFinal):
        arq.write(str(beat*gerados) + "")
        gerados = gerados +1
        beatatual = beat*gerados
    else:
        arq.write(str(beat*gerados) + ",")
        gerados = gerados +1
        beatatual = beat*gerados
            
arq.write('],\\"signatures\\":[{\\"__class\\":\\"MusicSignature\\",\\"marker\\":0,\\"beats\\":4}],\\"startBeat\\":' + str(startBeat) + ',\\"endBeat\\":' + str(endBeat) + ',\\"fadeStartBeat\\":0,\\"useFadeStartBeat\\":false,\\"fadeEndBeat\\":0,\\"useFadeEndBeat\\":false,\\"videoStartTime\\":0,\\"previewEntry\\":0,\\"previewLoopStart\\":0,\\"previewLoopEnd\\":48,\\"volume\\":0,\\"fadeInDuration\\":0,\\"fadeInType\\":0,\\"fadeOutDuration\\":0,\\"fadeOutType\\":0},\\"path\\":\\"\\",\\"url\\":\\"jmcs://jd-contents/' + CodeName.lower() + '/' + CodeName.lower() + '_AudioPreview.ogg\\"}",')
arq.write('"coachCount": ' + str(CoachCount) + ',')
arq.write('"credits": "All rights of the producer and other rightholders to the recorded work reserved. Unless otherwise authorized, the duplication, rental, loan, exchange or use of this video game for public performance, broadcasting and online distribution to the public are prohibited.",')
if (LocaleID == "yes"):
    arq.write('"customTypeNameId": 0,')
arq.write('"difficulty": ' + str(Difficulty) + ',')
arq.write('"doubleScoringType": -1,')
arq.write('"jdmAttributes": [],')
arq.write('"lyricsColor": ' + '"' + LyricsColor + 'FF",')
arq.write('"lyricsType": ' + str(LyricsType) + ',')
arq.write('"mainCoach": -1,')
arq.write('"mapLength": 0,')
arq.write('"mapName": ' + '"' + CodeName + '",')
arq.write('"mapPreviewMpd": "<?xml version=\\"1.0\\"?>\\r\\n<MPD xmlns:xsi=\\"http://www.w3.org/2001/XMLSchema-instance\\" xmlns=\\"urn:mpeg:DASH:schema:MPD:2011\\" xsi:schemaLocation=\\"urn:mpeg:DASH:schema:MPD:2011\\" type=\\"static\\" mediaPresentationDuration=\\"PT30S\\" minBufferTime=\\"PT1S\\" profiles=\\"urn:webm:dash:profile:webm-on-demand:2012\\">\\r\\n\\t<Period id=\\"0\\" start=\\"PT0S\\" duration=\\"PT30S\\">\\r\\n\\t\\t<AdaptationSet id=\\"0\\" mimeType=\\"video/webm\\" codecs=\\"vp8\\" lang=\\"eng\\" maxWidth=\\"720\\" maxHeight=\\"370\\" subsegmentAlignment=\\"true\\" subsegmentStartsWithSAP=\\"1\\" bitstreamSwitching=\\"true\\">\\r\\n\\t\\t\\t<Representation id=\\"0\\" bandwidth=\\"495888\\">\\r\\n\\t\\t\\t\\t<BaseURL>jmcs://jd-contents/' + CodeName + '/' + CodeName + '_MapPreviewNoSoundCrop_LOW.vp8.webm</BaseURL>\\r\\n\\t\\t\\t\\t<SegmentBase indexRange=\\"588-1077\\">\\r\\n\\t\\t\\t\\t\\t<Initialization range=\\"0-588\\" />\\r\\n\\t\\t\\t\\t</SegmentBase>\\r\\n\\t\\t\\t</Representation>\\r\\n\\t\\t\\t<Representation id=\\"1\\" bandwidth=\\"1476873\\">\\r\\n\\t\\t\\t\\t<BaseURL>jmcs://jd-contents/' + CodeName + '/' + CodeName + '_MapPreviewNoSoundCrop_MID.vp8.webm</BaseURL>\\r\\n\\t\\t\\t\\t<SegmentBase indexRange=\\"585-1075\\">\\r\\n\\t\\t\\t\\t\\t<Initialization range=\\"0-585\\" />\\r\\n\\t\\t\\t\\t</SegmentBase>\\r\\n\\t\\t\\t</Representation>\\r\\n\\t\\t\\t<Representation id=\\"2\\" bandwidth=\\"2916702\\">\\r\\n\\t\\t\\t\\t<BaseURL>jmcs://jd-contents/' + CodeName + '/' + CodeName + '_MapPreviewNoSoundCrop_HIGH.vp8.webm</BaseURL>\\r\\n\\t\\t\\t\\t<SegmentBase indexRange=\\"585-1075\\">\\r\\n\\t\\t\\t\\t\\t<Initialization range=\\"0-585\\" />\\r\\n\\t\\t\\t\\t</SegmentBase>\\r\\n\\t\\t\\t</Representation>\\r\\n\\t\\t\\t<Representation id=\\"3\\" bandwidth=\\"4055531\\">\\r\\n\\t\\t\\t\\t<BaseURL>jmcs://jd-contents/' + CodeName + '/' + CodeName + '_MapPreviewNoSoundCrop_ULTRA.vp8.webm</BaseURL>\\r\\n\\t\\t\\t\\t<SegmentBase indexRange=\\"585-1075\\">\\r\\n\\t\\t\\t\\t\\t<Initialization range=\\"0-585\\" />\\r\\n\\t\\t\\t\\t</SegmentBase>\\r\\n\\t\\t\\t</Representation>\\r\\n\\t\\t</AdaptationSet>\\r\\n\\t</Period>\\r\\n</MPD>\\r\\n",')
arq.write('"mode": 6,')
arq.write('"originalJDVersion": ' + str(OriginalJDVersion) + ',')
arq.write('"packages": { "mapContent": "' + CodeName + '_mapContent" },')
arq.write('"parentMapName": ' + '"' + CodeName + '",')
arq.write('"skuIds": ["jdcmos-ww-all"],')
arq.write('"songColors": {"songColor_1A": "4E008AFF", "songColor_1B": "3C00B7FF", "songColor_2A": "00CAFDFF", "songColor_2B": "EDAA02FF"},')
arq.write('"status": 3,')
arq.write('"sweatDifficulty": 1,')
arq.write('"tags": ["Main", "subscribedSong"],')
arq.write('"title": "' + Title + '",')
arq.write('"urls": { "jmcs://jd-contents/' + CodeName + '/' + CodeName + '_AudioPreview.ogg": "" },')
arq.write('"searchTags": [],')
arq.write('"searchTagsLocIds": [],')
arq.write('"serverChangelist": 0')
arq.write('}')
arq.close()