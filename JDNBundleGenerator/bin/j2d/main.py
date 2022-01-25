import json
import os
import sys
import math

codename = sys.argv[1]

input_json = "bin/j2d/input/input.json"
moves0_json = "bin/j2d/input/inputmoves.json"
moves1_json = "bin/j2d/input/inputmovesp2.json"
moves2_json = "bin/j2d/input/inputmovesp3.json"
moves3_json = "bin/j2d/input/inputmovesp4.json"
songpreviewbeats_json = "bin/j2d/input/input_SongPreviewBeats.json"
musictrack_name = "input/" + codename + "/" + codename.lower() + "_musictrack.tpl.ckd"
ktape_name = "input/" + codename + "/" + codename.lower() + "_tml_karaoke.ktape.ckd"
dtape_name = "input/" + codename + "/" + codename.lower() + "_tml_dance.dtape.ckd"
with open(input_json, "r") as a:
    input_data = json.load(a)
    a.close()
with open(moves0_json, "r") as b:
    moves0_data = json.load(b)
    b.close()
try:
    with open(moves1_json, "r") as c:
        moves1_data = json.load(c)
        c.close()
except FileNotFoundError:
    moves1_data = "[]"
try:
    with open(moves2_json, "r") as d:
        moves2_data = json.load(d)
        d.close()
except FileNotFoundError:
    moves2_data = "[]"
try:
    with open(moves3_json, "r") as e:
        moves3_data = json.load(e)
        e.close()
except FileNotFoundError:
    moves3_data = "[]"
try:
    with open(songpreviewbeats_json) as g:
        songpreviewbeats_data = json.load(g)
        g.close()
except FileNotFoundError:
    songpreviewbeats_data = "[]"
division = 2502.66305525460462 / (60000 / (input_data['beats'][30] - input_data['beats'][29]))
# musictrack creator start
def beatsgen(number): return number*48
beats_ready = list(map(beatsgen, input_data['beats']))
endBeat_ready = len(input_data['beats'])
# preview thing for jdvs / division or input info
if songpreviewbeats_data == "[]":
    try:
        previewEntry_ready = input_data['AudioPreview']['coverflow']['startbeat']
        previewLoopStart_ready = input_data['AudioPreview']['coverflow']['startbeat']
        previewLoopEnd_ready = len(input_data['beats'])
    except KeyError:
        previewEntry_ready = input_data['AudioPreview']['prelobby']['startbeat']
        previewLoopStart_ready = input_data['AudioPreview']['prelobby']['startbeat']
        previewLoopEnd_ready = len(input_data['beats'])
else:
    previewEntry_ready = int(songpreviewbeats_data['enterTime'] / division)
    previewLoopStart_ready = int(songpreviewbeats_data['loopStartTime'] / division)
    previewLoopEnd_ready = int(songpreviewbeats_data['loopEndTime'] / division)
# all things ready, making musictrack time
musictrack = '{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"MusicTrackComponent_Template","trackData":{"__class":"MusicTrackData","structure":{"__class":"MusicTrackStructure","markers":' + str(beats_ready) + ',"signatures":[{"__class":"MusicSignature","marker":1,"beats":3},{"__class":"MusicSignature","marker":4,"beats":4},{"__class":"MusicSignature","marker":194,"beats":3},{"__class":"MusicSignature","marker":197,"beats":4}],"sections":[{"__class":"MusicSection","marker":1,"sectionType":6,"comment":""},{"__class":"MusicSection","marker":19,"sectionType":1,"comment":""},{"__class":"MusicSection","marker":52,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":68,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":84,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":100,"sectionType":1,"comment":""},{"__class":"MusicSection","marker":132,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":148,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":164,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":190,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":196,"sectionType":2,"comment":""},{"__class":"MusicSection","marker":194,"sectionType":6,"comment":""},{"__class":"MusicSection","marker":259,"sectionType":3,"comment":""},{"__class":"MusicSection","marker":195,"sectionType":7,"comment":""},{"__class":"MusicSection","marker":291,"sectionType":7,"comment":""}],"startBeat":0,"endBeat":' + str(endBeat_ready) + ',"videoStartTime":0,"previewEntry":' + str(previewEntry_ready) + ',"previewLoopStart":' + str(previewLoopStart_ready) + ',"previewLoopEnd":' + str(previewLoopEnd_ready) + ',"volume":0},"path":"world/maps/' + codename.lower() + '/audio/' + codename.lower() + '.wav","url":"jmcs://jd-contents/' + codename + '/' + codename + '.ogg"}}]}'
with open(musictrack_name, "w") as h:
    h.write(musictrack)
    h.close()
# musictrack creator end
# ktape creator start
i = 0
ktape_clips = "["
while i < len(input_data['lyrics'][1:-1]):
    ktape_clip_time = input_data['lyrics'][i]['time']
    ktape_duration_time = input_data['lyrics'][i]['duration']
    ktape_text_time = input_data['lyrics'][i]['text']
    try:
        ktape_isLineEnding_time = input_data['lyrics'][i]['isLineEnding']
    except KeyError:
        ktape_isLineEnding_time = 0
    ktape_clip_time_ready = int(ktape_clip_time / division)
    ktape_duration_time_ready = int(ktape_duration_time / division)
    ktape_clip_ready = '{"__class":"KaraokeClip","Id":' + str(i * 11002332) + ',"TrackId":' + str(11002332) + ',"IsActive":1,"StartTime":' + str(ktape_clip_time_ready) + ',"Duration":' + str(ktape_duration_time_ready) + ',"Pitch":8.661958,"Lyrics":"' + ktape_text_time + '","IsEndOfLine":' + str(ktape_isLineEnding_time) + ',"ContentType":0,"StartTimeTolerance":4,"EndTimeTolerance":4,"SemitoneTolerance":5}'
    ktape_clips += ktape_clip_ready + ","
    i += 1
ktape_clips = ktape_clips + "]"
ktape_clips = ktape_clips.replace(",]","]")
ktape = '{"__class":"Tape","Clips":' + str(ktape_clips) + ',"TapeClock":0,"TapeBarCount":1,"FreeResourcesAfterPlay":0,"MapName":"' + codename + '"}'
with open(ktape_name, "w") as h:
    h.write(ktape)
    h.close()
# ktape creator end
# dtape creator start
i = 0
dtape_clips = "["
while i < len(moves0_data[1:-1]):
    dtape_motionclip_name = moves0_data[i]['name']
    dtape_motionclip_time = moves0_data[i]['time']
    try:
        dtape_motionclip_goldmove = moves0_data[i]['goldMove']
    except KeyError:
        dtape_motionclip_goldmove = 0
    dtape_motionclip_duration = moves0_data[i]['duration']
    dtape_motionclip_time_ready = int(dtape_motionclip_time / division)
    dtape_motionclip_duration_ready = int(dtape_motionclip_duration / division)
    dtape_motionclip_classifierpath_ready = 'world/maps/' + codename.lower() + '/timeline/moves/' + dtape_motionclip_name + '.msm'
    dtape_motionclip_ready = '{"__class":"MotionClip","Id":' + str(i * 11002332) + ',"TrackId":' + str(11002332) + ',"IsActive":1,"StartTime":' + str(dtape_motionclip_time_ready) + ',"Duration":' + str(dtape_motionclip_duration_ready) + ',"ClassifierPath":"' + dtape_motionclip_classifierpath_ready + '","GoldMove":' + str(dtape_motionclip_goldmove) + ',"CoachId":0,"MoveType":0,"Color":[1,0.988235,0.670588,0.870588],"MotionPlatformSpecifics":{"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0},"DURANGO":{"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0}}}'
    dtape_clips += dtape_motionclip_ready + ","
    i += 1
i = 0
if moves1_data == "[]":
    dtape_clips = dtape_clips
else:
    while i < len(moves1_data[1:-1]):
        dtape_motionclip_name = moves1_data[i]['name']
        dtape_motionclip_time = moves1_data[i]['time']
        try:
            dtape_motionclip_goldmove = moves1_data[i]['goldMove']
        except KeyError:
            dtape_motionclip_goldmove = 0
        dtape_motionclip_duration = moves1_data[i]['duration']
        dtape_motionclip_time_ready = int(dtape_motionclip_time / division)
        dtape_motionclip_duration_ready = int(dtape_motionclip_duration / division)
        dtape_motionclip_classifierpath_ready = 'world/maps/' + codename.lower() + '/timeline/moves/' + dtape_motionclip_name + '.msm'
        dtape_motionclip_ready = '{"__class":"MotionClip","Id":' + str(i * 11002332) + ',"TrackId":' + str(11002332) + ',"IsActive":1,"StartTime":' + str(dtape_motionclip_time_ready) + ',"Duration":' + str(dtape_motionclip_time_ready) + ',"ClassifierPath":"' + dtape_motionclip_classifierpath_ready + '","GoldMove":' + str(dtape_motionclip_goldmove) + ',"CoachId":1,"MoveType":0,"Color":[1,0.988235,0.670588,0.870588],"MotionPlatformSpecifics":{"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0},"DURANGO":{"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0}}}'
        dtape_clips += dtape_motionclip_ready + ","
        i += 1
if moves2_data == "[]":
    dtape_clips = dtape_clips
else:
    while i < len(moves2_data[1:-1]):
        dtape_motionclip_name = moves2_data[i]['name']
        dtape_motionclip_time = moves2_data[i]['time']
        try:
            dtape_motionclip_goldmove = moves2_data[i]['goldMove']
        except KeyError:
            dtape_motionclip_goldmove = 0
        dtape_motionclip_duration = moves2_data[i]['duration']
        dtape_motionclip_time_ready = int(dtape_motionclip_time / division)
        dtape_motionclip_duration_ready = int(dtape_motionclip_duration / division)
        dtape_motionclip_classifierpath_ready = 'world/maps/' + codename.lower() + '/timeline/moves/' + dtape_motionclip_name + '.msm'
        dtape_motionclip_ready = '{"__class":"MotionClip","Id":' + str(i * 11002332) + ',"TrackId":' + str(11002332) + ',"IsActive":1,"StartTime":' + str(dtape_motionclip_time_ready) + ',"Duration":' + str(dtape_motionclip_duration_ready) + ',"ClassifierPath":"' + dtape_motionclip_classifierpath_ready + '","GoldMove":' + str(dtape_motionclip_goldmove) + ',"CoachId":2,"MoveType":0,"Color":[1,0.988235,0.670588,0.870588],"MotionPlatformSpecifics":{"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0},"DURANGO":{"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0}}}'
        dtape_clips += dtape_motionclip_ready + ","
        i += 1
if moves3_data == "[]":
    dtape_clips = dtape_clips
else:
    while i < len(moves3_data[1:-1]):
        dtape_motionclip_name = moves3_data[i]['name']
        dtape_motionclip_time = moves3_data[i]['time']
        try:
            dtape_motionclip_goldmove = moves3_data[i]['goldMove']
        except KeyError:
            dtape_motionclip_goldmove = 0
        dtape_motionclip_duration = moves3_data[i]['duration']
        dtape_motionclip_time_ready = int(dtape_motionclip_time / division)
        dtape_motionclip_duration_ready = int(dtape_motionclip_duration / division)
        dtape_motionclip_classifierpath_ready = 'world/maps/' + codename.lower() + '/timeline/moves/' + dtape_motionclip_name + '.msm'
        dtape_motionclip_ready = '{"__class":"MotionClip","Id":' + str(i * 11002332) + ',"TrackId":' + str(11002332) + ',"IsActive":1,"StartTime":' + str(dtape_motionclip_time_ready) + ',"Duration":' + str(dtape_motionclip_duration_ready) + ',"ClassifierPath":"' + dtape_motionclip_classifierpath_ready + '","GoldMove":' + str(dtape_motionclip_goldmove) + ',"CoachId":3,"MoveType":0,"Color":[1,0.988235,0.670588,0.870588],"MotionPlatformSpecifics":{"X360": {"__class": "MotionPlatformSpecific","ScoreScale": 1,"ScoreSmoothing": 0,"ScoringMode": 0},"ORBIS": {"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0},"DURANGO":{"__class":"MotionPlatformSpecific","ScoreScale":1,"ScoreSmoothing":0,"ScoringMode":0}}}'
        dtape_clips += dtape_motionclip_ready + ","
        i += 1
i = 0
while i < len(input_data['pictos'][1:-1]):
    dtape_pictogramclip_name = input_data['pictos'][i]['name']
    dtape_pictogramclip_time = input_data['pictos'][i]['time']
    dtape_pictogramclip_duration = input_data['pictos'][i]['duration']
    dtape_pictogramclip_time_ready = int(dtape_pictogramclip_time / division)
    dtape_pictogramclip_duration_ready = int(dtape_pictogramclip_duration / division)
    dtape_pictogramclip_pictopath_ready = 'world/maps/' + codename.lower() + '/timeline/pictos/' + dtape_pictogramclip_name + '.tga'
    dtape_pictogramclip_ready = '{"__class":"PictogramClip","Id":' + str(i * 11002332) + ',"TrackId":' + str(11002332) + ',"IsActive":1,"StartTime":' + str(dtape_pictogramclip_time_ready) + ',"Duration":' + str(dtape_pictogramclip_duration_ready) + ',"PictoPath":"' + dtape_pictogramclip_pictopath_ready + '","MontagePath":"","AtlIndex":4294967295,"CoachCount":4294967295}'
    dtape_clips += dtape_pictogramclip_ready + ","
    i += 1
dtape_clips = dtape_clips + "]"
dtape_clips = dtape_clips.replace(",]","]")
dtape = '{"__class":"Tape","Clips":' + dtape_clips + ',"TapeClock":0,"TapeBarCount":1,"FreeResourcesAfterPlay":0,"MapName":"' + codename + '"}'
with open(dtape_name, "w") as h:
    h.write(dtape)
    h.close()
# dtape creator end
print("Title: " + input_data['Title'])
print("Artist: " + input_data['Artist'])
print('Division: ' + str(division))
# YAS I'M FINISHED THIS SHIT SDKAJFPKSDJKPFJSDAPFJKSPDAPKJSDA
