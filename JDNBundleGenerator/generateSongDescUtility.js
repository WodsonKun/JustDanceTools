var fs = require("fs")
const http = require('http');

let codename = ''
let coachcount = ''
codename = process.argv[2]
coachcount = parseInt(process.argv[3])

console.log('\x1b[36m%s\x1b[0m', "---- GENERATE SONGDESC UTILITY ----" + '\n')
console.log("Running..." + '\n')

var base = "http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/"

var JSONP_PREFIX = /^[^(]*?\(/;
var JSONP_SUFFIX = /\)[^)]*?$/;
function parsejsonp(jsonpString) {
    var prefix = jsonpString.match(JSONP_PREFIX)[0];
    var suffix = jsonpString.match(JSONP_SUFFIX)[0];
    return JSON.parse(jsonpString.substring(prefix.length, jsonpString.length - suffix.length));
}

http.get(base + "songs/" + codename + "/" + codename + ".json", res => {
    let data = ""

        res.on("data", d => {
        data += d
    })
        res.on("end", () => {
		const songjson = parsejsonp(data)
		let jdVersion = ''
		let OriginaljdVersion = ''
		let phoneImages = ''
		if (songjson.JDVersion) {
			jdVersion = songjson.JDVersion
		}
		if (!songjson.JDVersion || songjson.JDVersion === 0 || songjson.JDVersion == 0) {
			jdVersion = 2017
		}
		if (songjson.OriginalJDVersion) {
			OriginaljdVersion = songjson.OriginalJDVersion
		}
		if (!songjson.OriginalJDVersion || songjson.OriginalJDVersion === 0 || songjson.OriginalJDVersion == 0) {
			OriginaljdVersion = 2017
		}
		
		if (coachcount == 1) {
			phoneImages = {
			"cover": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_cover_phone.jpg",
            "coach1": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_1_phone.png"
			}
		}
		if (coachcount == 2) {
			phoneImages = {
			"cover": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_cover_phone.jpg",
            "coach1": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_1_phone.png",
			"coach2": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_2_phone.png"
			}
		}
		if (coachcount == 3) {
			phoneImages = {
			"cover": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_cover_phone.jpg",
            "coach1": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_1_phone.png",
			"coach2": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_2_phone.png",
			"coach3": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_3_phone.png"
			}
		}
		if (coachcount == 4) {
			phoneImages = {
			"cover": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_cover_phone.jpg",
            "coach1": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_1_phone.png",
			"coach2": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_2_phone.png",
			"coach3": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_3_phone.png",
			"coach4": "world/maps/"+codename.toLowerCase()+ "/menuart/textures/"+codename.toLowerCase()+"_coach_4_phone.png"
			}
		}

		let songdescription = {
    "__class": "Actor_Template",
    "WIP": 0,
    "LOWUPDATE": 0,
    "UPDATE_LAYER": 0,
    "PROCEDURAL": 0,
    "STARTPAUSED": 0,
    "FORCEISENVIRONMENT": 0,
    "COMPONENTS": [{
            "__class": "JD_SongDescTemplate",
            "MapName": codename,
            "JDVersion": jdVersion,
            "OriginalJDVersion": OriginaljdVersion,
            "Artist": songjson.Artist,
            "DancerName": "Unknown Dancer",
            "Title": songjson.Title,
            "Credits": "All rights of the producer and other rightholders to the recorded work reserved. Unless otherwise authorized, the duplication, rental, loan, exchange or use of this video game for public performance, broadcasting and online distribution to the public are prohibited.",
            "PhoneImages": phoneImages,
            "NumCoach": coachcount,
            "MainCoach": -1,
            "Difficulty": 2,
            "SweatDifficulty": 1,
            "backgroundType": 0,
            "LyricsType": 0,
            "Tags": ["Main"],
            "Status": 3,
            "LocaleID": 4294967295,
            "MojoValue": 0,
            "CountInProgression": 1,
            "DefaultColors": {
                "songcolor_2a": [1, 1, 0, 0.823529],
                "lyrics": [1, 0.192157, 0.823529, 0.945098],
                "theme": [1, 1, 1, 1],
                "songcolor_1a": [1, 0.098039, 0, 0.596078],
                "songcolor_2b": [1, 0, 0.054902, 0.258824],
                "songcolor_1b": [1, 0, 0.117647, 0.211765]
            },
            "VideoPreviewPath": ""
        }
    ]
}
	fs.writeFileSync("input/" + codename + "/songdesc.tpl.ckd", JSON.stringify(songdescription))

    })
	console.log("Generated songDesc!" + '\n')
})