const {
    exec
} = require("child_process");
const fs = require('fs');

let codename = ''
    let coachcount = ''
    codename = process.argv[2]
    coachcount = process.argv[3]
    var codenamelower = codename.toLowerCase()
    console.log('\x1b[36m%s\x1b[0m', "---- PICTO CONTROLLER UTILITY ----" + '\n')
    console.log("Running..." + '\n')
    console.log("This might take a while...")
    console.log("(seriously)" + '\n')

var pcHeader = "00000009544558000000002C000020800100010000011800000020800000000000010000000000000000CCCC"
    var pngPath = `./bin/pictos/${codename}/pictos/`
    var ddsPath = `./bin/pictos/${codename}/pictos/dds`
    var ckdPath = `./bin/pictos/${codename}/pictos/ckd`

    var pictoDir = fs.readdirSync(pngPath)

    pictoDir.forEach(pictos => {
    if (pictos.endsWith(".png")) {
        exec(`bin\\converters\\nvcompress.exe ` + `-bc3` + ` bin\\pictos\\${codename}\\pictos\\` + pictos + ` bin\\pictos\\${codename}\\pictos\\dds\\` + pictos + ".dds", (error, stdout, stderr) => {
            if (error) {
                console.log(`Error with png2DDS: ${error.message}`);
                return;
            }
            if (stderr) {
                console.log(`Generated IPK for codename, size: `);
                return;
            }
        })
    } else {}
})
