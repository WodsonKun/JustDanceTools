const fs = require('fs');
const http = require('http');
const axios = require('axios');

let codename = ''
let coachcount = ''
codename = process.argv[2]
coachcount = process.argv[3]
console.log('\x1b[36m%s\x1b[0m', "---- DOWNLOAD DATA UTILITY ----" + '\n')
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
			console.log("Downloaded base JSON!" + '\n')
        fs.writeFileSync("./bin/j2d/input/input.json", JSON.stringify(parsejsonp(data), 2, null))

    })
})

if (coachcount == 4) {
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves0.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves0!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmoves.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves1.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves1!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmovesp2.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves2.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves2!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmovesp3.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves3.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves3!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmovesp4.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })

}

if (coachcount == 3) {
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves0.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves0!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmoves.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves1.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves1!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmovesp2.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves2.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves2!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmovesp3.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })

}

if (coachcount == 2) {
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves0.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves0!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmoves.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves1.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
				console.log("Downloaded moves1!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmovesp2.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })

}

if (coachcount == 1) {
    http.get(base + "songs/" + codename + "/data/moves/" + codename + "_moves0.json", res => {
        let data = ""

            res.on("data", d => {
            data += d
        })
            res.on("end", () => {
			console.log("Downloaded moves0!" + '\n')
            fs.writeFileSync("./bin/j2d/input/inputmoves.json", JSON.stringify(parsejsonp(data), 2, null))

        })
    })

}