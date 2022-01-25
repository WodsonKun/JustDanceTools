var fs = require("fs")
let codename = ''
let coachcount = ''
codename = process.argv[2]
coachcount = process.argv[3]
var path = "./input/" + codename +"/textures/" 
var direc = fs.readdirSync(path)
console.log('\x1b[36m%s\x1b[0m', "---- TEXTURE RENAME UTILITY ----" + '\n')
console.log("Running..." + '\n')

console.log("CoachCount is " + coachcount + '\n')
direc.forEach(files => {
    console.log(files + " -> " + codename.toLowerCase() + files.substring(8))
	fs.renameSync(path + files, path + codename.toLowerCase() + files.substring(8))
}) 
console.log("Done!" + '\n')