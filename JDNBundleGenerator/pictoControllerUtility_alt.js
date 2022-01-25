const {
    exec
} = require("child_process");
const fs = require('fs');
let codename = ''
    let coachcount = ''
    codename = process.argv[2]
    coachcount = process.argv[3]
    var codenamelower = codename.toLowerCase()
    var pcHeader = "00000009544558000000002C000020800100010000011800000020800000000000010000000000000000CCCC"
    var pngPath = `./bin/pictos/${codename}/pictos/`
    var ddsPath = `./bin/pictos/${codename}/pictos/dds`
    var ckdPath = `./bin/pictos/${codename}/pictos/ckd`
	var pictoDDSDir = fs.readdirSync(ddsPath)
    pictoDDSDir.forEach(pictos1 => {
    if (pictos1.endsWith(".dds")) {
        var ddsWithTga = pcHeader + fs.readFileSync(ddsPath + "/" + pictos1).toString("hex")
            fs.writeFileSync(ckdPath + "/" + pictos1.split(".")[0] + ".tga.ckd", Buffer.from(ddsWithTga, "hex"), function (err) {
            console.log(err)
        })
    } else {}
})
