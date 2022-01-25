var fs = require("fs");

let codename = ''
let coachcount = ''
let platform = ''
codename = process.argv[2]
platform = process.argv[4]
coachcount = process.argv[3]


const codenamelower = codename.toLowerCase()
var cachePath = "./output_mainscene/" + codename + "/cache/itf_cooked/" + platform.toLowerCase() + "/world/maps/" + codenamelower
var worldPath = "./output_mainscene/" + codename + "/world/maps/" + codenamelower

const { mkdir } = require('fs').promises;

fs.mkdirSync(cachePath, { recursive: true }, (err) => {
    if (err) throw err;
});

fs.mkdirSync(worldPath, { recursive: true }, (err) => {
    if (err) throw err;
});

(async function main() {
  try {
    const cacheDirs  = ['audio', 'cinematics', 'autodance', 'timeline/pictos', "videoscoach", "graph", "menuart", "menuart/actors", "menuart/textures"];

    await Promise.all(
      cacheDirs.map(dirname => fs.mkdirSync(`${cachePath}/${dirname}`, { recursive: true }))
    );

  } catch (err) {
    console.log(err);
  }
})();

fs.mkdirSync(`${worldPath}/videoscoach`, { recursive: true })
fs.mkdirSync(`${worldPath}/autodance`, { recursive: true })
fs.mkdirSync(`${worldPath}/timeline/moves/wiiu/`, { recursive: true })

function getHex(num) {
  return (`00000000` + num.toString(16)).substr(-8);
}

var mainTape = `{"__class":"Tape","Clips":[],"TapeClock":0,"TapeBarCount":1,"FreeResourcesAfterPlay":0,"MapName":"${codename}"}`

var audioisc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="MusicTrack" MARKER="" POS2D="1.125962 -0.418641" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_musictrack.tpl">
				<COMPONENTS NAME="MusicTrackComponent">
					<MusicTrackComponent />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_sequence" MARKER="" POS2D="-0.006158 -0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_sequence.tpl">
				<COMPONENTS NAME="TapeCase_Component">
					<TapeCase_Component />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`

var sequence = `{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"TapeCase_Template","TapesRack":[{"__class":"TapeGroup","Entries":[{"__class":"TapeEntry","Label":"TML_Sequence","Path":"world/maps/${codenamelower}/audio/${codenamelower}.stape"}]}]}]} `

fs.writeFileSync(cachePath + "/audio/" + codenamelower + ".stape.ckd", mainTape, function(err) {
    console.log(err)
});
fs.writeFileSync(cachePath + "/audio/" + codenamelower + "_audio.isc.ckd", audioisc, function(err) {
    console.log(err)
});
fs.writeFileSync(cachePath + "/audio/" + codenamelower + "_sequence.tpl.ckd", sequence, function(err) {
    console.log(err)
});

// cinematics

var cine = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_MainSequence" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/cinematics/${codenamelower}_mainsequence.tpl">
				<COMPONENTS NAME="MasterTape">
					<MasterTape />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`
var mainsequence_tpl = `{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"MasterTape_Template","TapesRack":[{"__class":"TapeGroup","Entries":[{"__class":"TapeEntry","Label":"master","Path":"world/maps/${codenamelower}/cinematics/${codenamelower}_mainsequence.tape"}]}]}]} `

fs.writeFileSync(cachePath + "/cinematics/" + codenamelower + "_cine.isc.ckd", cine, function(err) {
    console.log(err)
});

fs.writeFileSync(cachePath + "/cinematics/" + codenamelower + "_mainsequence.tape.ckd", mainTape, function(err) {
    console.log(err)
});

fs.writeFileSync(cachePath + "/cinematics/" + codenamelower + "_mainsequence.tpl.ckd", mainsequence_tpl, function(err) {
    console.log(err)
});

var graph = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="10.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="Camera_JD_Dummy" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_emptyactor.tpl" />
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`

fs.writeFileSync(cachePath + "/graph/" + codenamelower + "_graph.isc.ckd", graph, function(err) {
    console.log(err)
});


let menuart_isc = ""
if (coachcount === 1) {
	menuart_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`
}
if (coachcount === 2) {
	menuart_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_2" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_2.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`
}
if (coachcount === 3) {
	menuart_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_2" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_2.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_3" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_3.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`
}
if (coachcount === 4) {
	menuart_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_2" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_2.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_3" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_3.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_4" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="6" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_4.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="6" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
				<COMPONENTS NAME="MaterialGraphicComponent">
					<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</MaterialGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>`
}

fs.writeFileSync(cachePath + "/menuart/" + codenamelower + "_menuart.isc.ckd", menuart_isc, function(err) {
    console.log(err)
});

var tml_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_dance" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.tpl">
				<COMPONENTS NAME="TapeCase_Component">
					<TapeCase_Component />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_karaoke" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.tpl">
				<COMPONENTS NAME="TapeCase_Component">
					<TapeCase_Component />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`

fs.writeFileSync(cachePath + "/timeline/" + codenamelower + "_tml.isc.ckd", tml_isc, function(err) {
    console.log(err)
});

var dance_tpl = `{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"TapeCase_Template","TapesRack":[{"__class":"TapeGroup","Entries":[{"__class":"TapeEntry","Label":"TML_Motion","Path":"world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.dtape"}]}]}]} `

fs.writeFileSync(cachePath + "/timeline/" + codenamelower + "_tml_dance.tpl.ckd", dance_tpl, function(err) {
    console.log(err)
});

var karaoke_tpl = `{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"TapeCase_Template","TapesRack":[{"__class":"TapeGroup","Entries":[{"__class":"TapeEntry","Label":"TML_karaoke","Path":"world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.ktape"}]}]}]} `

fs.writeFileSync(cachePath + "/timeline/" + codenamelower + "_tml_karaoke.tpl.ckd", karaoke_tpl, function(err) {
    console.log(err)
});

var video_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="-1.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="VideoScreen" MARKER="" POS2D="0.000000 -4.500000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_player_main.tpl">
				<COMPONENTS NAME="PleoComponent">
					<PleoComponent video="world/maps/${codenamelower}/videoscoach/${codenamelower}.webm" dashMPD="world/maps/${codenamelower}/videoscoach/${codenamelower}.mpd" channelID="" />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="3.941238 2.220000" xFLIPPED="0" USERFRIENDLY="VideoOutput" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_output_mainscene_main.tpl">
				<COMPONENTS NAME="PleoTextureGraphicComponent">
					<PleoTextureGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000" channelID="">
						<PrimitiveParameters>
							<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
								<ENUM NAME="gfxOccludeInfo" SEL="0" />
							</GFXPrimitiveParam>
						</PrimitiveParameters>
						<ENUM NAME="anchor" SEL="1" />
						<material>
							<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/pleofullscreen.msh" stencilTest="0" alphaTest="0" alphaRef="0">
								<textureSet>
									<GFXMaterialTexturePathSet diffuse="" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
								</textureSet>
								<materialParams>
									<GFXMaterialSerializableParam Reflector_factor="0.000000" />
								</materialParams>
							</GFXMaterialSerializable>
						</material>
						<ENUM NAME="oldAnchor" SEL="1" />
					</PleoTextureGraphicComponent>
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`

fs.writeFileSync(cachePath + "/videoscoach/" + codenamelower + "_video.isc.ckd", video_isc, function(err) {
    console.log(err)
});

let mainscene_isc = ""
if (coachcount == 1) {
	mainscene_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="2.000000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<PLATFORM_FILTER>
			<TargetFilterList platform="WII">
				<objects VAL="${codename}_AUTODANCE" />
			</TargetFilterList>
		</PLATFORM_FILTER>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUDIO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/audio/${codenamelower}_audio.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="MusicTrack" MARKER="" POS2D="1.125962 -0.418641" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_musictrack.tpl">
								<COMPONENTS NAME="MusicTrackComponent">
									<MusicTrackComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_sequence" MARKER="" POS2D="-0.006158 -0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_sequence.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_CINE" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/cinematics/${codenamelower}_cine.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_MainSequence" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/cinematics/${codenamelower}_mainsequence.tpl">
								<COMPONENTS NAME="MasterTape">
									<MasterTape />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_GRAPH" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/graph/${codenamelower}_graph.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="10.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="Camera_JD_Dummy" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_emptyactor.tpl" />
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_TML" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/timeline/${codenamelower}_tml.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_dance" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_karaoke" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_VIDEO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/videoscoach/${codenamelower}_video.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="-1.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="VideoScreen" MARKER="" POS2D="0.000000 -4.500000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_player_main.tpl">
								<COMPONENTS NAME="PleoComponent">
									<PleoComponent video="world/maps/${codenamelower}/videoscoach/${codenamelower}.webm" dashMPD="world/maps/${codenamelower}/videoscoach/${codenamelower}.mpd" channelID="" />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="3.941238 2.220000" xFLIPPED="0" USERFRIENDLY="VideoOutput" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_output_mainscene_main.tpl">
								<COMPONENTS NAME="PleoTextureGraphicComponent">
									<PleoTextureGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000" channelID="">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/pleofullscreen.msh" stencilTest="0" alphaTest="0" alphaRef="0">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</PleoTextureGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename} : Template Artist - Template Title&#10;JDVer = 5, ID = 842776738, Type = 1 (Flags 0x00000000), NbCoach = 2, Difficulty = 2" MARKER="" POS2D="-3.531976 -1.485322" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/songdesc.tpl">
				<COMPONENTS NAME="JD_SongDescComponent">
					<JD_SongDescComponent />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_menuart" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/menuart/${codenamelower}_menuart.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="3" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUTODANCE" MARKER="" POS2D="0.000000 -0.033823" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_autodance" MARKER="" POS2D="-0.006150 -0.003075" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.tpl">
								<COMPONENTS NAME="JD_AutodanceComponent">
									<JD_AutodanceComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0">
				<sceneConfigs NAME="JD_MapSceneConfig">
					<JD_MapSceneConfig name="" soundContext="" hud="0" phoneTitleLocId="4294967295" phoneImage="">
						<ENUM NAME="Pause_Level" SEL="6" />
						<ENUM NAME="type" SEL="1" />
						<ENUM NAME="musicscore" SEL="2" />
					</JD_MapSceneConfig>
				</sceneConfigs>
			</SceneConfigs>
		</sceneConfigs>
	</Scene>
</root>
`
}
if (coachcount == 2) {
	mainscene_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="2.000000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<PLATFORM_FILTER>
			<TargetFilterList platform="WII">
				<objects VAL="${codename}_AUTODANCE" />
			</TargetFilterList>
		</PLATFORM_FILTER>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUDIO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/audio/${codenamelower}_audio.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="MusicTrack" MARKER="" POS2D="1.125962 -0.418641" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_musictrack.tpl">
								<COMPONENTS NAME="MusicTrackComponent">
									<MusicTrackComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_sequence" MARKER="" POS2D="-0.006158 -0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_sequence.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_CINE" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/cinematics/${codenamelower}_cine.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_MainSequence" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/cinematics/${codenamelower}_mainsequence.tpl">
								<COMPONENTS NAME="MasterTape">
									<MasterTape />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_GRAPH" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/graph/${codenamelower}_graph.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="10.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="Camera_JD_Dummy" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_emptyactor.tpl" />
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_TML" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/timeline/${codenamelower}_tml.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_dance" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_karaoke" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_VIDEO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/videoscoach/${codenamelower}_video.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="-1.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="VideoScreen" MARKER="" POS2D="0.000000 -4.500000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_player_main.tpl">
								<COMPONENTS NAME="PleoComponent">
									<PleoComponent video="world/maps/${codenamelower}/videoscoach/${codenamelower}.webm" dashMPD="world/maps/${codenamelower}/videoscoach/${codenamelower}.mpd" channelID="" />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="3.941238 2.220000" xFLIPPED="0" USERFRIENDLY="VideoOutput" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_output_mainscene_main.tpl">
								<COMPONENTS NAME="PleoTextureGraphicComponent">
									<PleoTextureGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000" channelID="">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/pleofullscreen.msh" stencilTest="0" alphaTest="0" alphaRef="0">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</PleoTextureGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename} : Template Artist - Template Title&#10;JDVer = 5, ID = 842776738, Type = 1 (Flags 0x00000000), NbCoach = 2, Difficulty = 2" MARKER="" POS2D="-3.531976 -1.485322" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/songdesc.tpl">
				<COMPONENTS NAME="JD_SongDescComponent">
					<JD_SongDescComponent />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_menuart" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/menuart/${codenamelower}_menuart.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="3" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_2" MARKER="" POS2D="524.381104 670.829834" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_2.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUTODANCE" MARKER="" POS2D="0.000000 -0.033823" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_autodance" MARKER="" POS2D="-0.006150 -0.003075" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.tpl">
								<COMPONENTS NAME="JD_AutodanceComponent">
									<JD_AutodanceComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0">
				<sceneConfigs NAME="JD_MapSceneConfig">
					<JD_MapSceneConfig name="" soundContext="" hud="0" phoneTitleLocId="4294967295" phoneImage="">
						<ENUM NAME="Pause_Level" SEL="6" />
						<ENUM NAME="type" SEL="1" />
						<ENUM NAME="musicscore" SEL="2" />
					</JD_MapSceneConfig>
				</sceneConfigs>
			</SceneConfigs>
		</sceneConfigs>
	</Scene>
</root>
`
}
if (coachcount == 3) {
	mainscene_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="2.000000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<PLATFORM_FILTER>
			<TargetFilterList platform="WII">
				<objects VAL="${codename}_AUTODANCE" />
			</TargetFilterList>
		</PLATFORM_FILTER>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUDIO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/audio/${codenamelower}_audio.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="MusicTrack" MARKER="" POS2D="1.125962 -0.418641" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_musictrack.tpl">
								<COMPONENTS NAME="MusicTrackComponent">
									<MusicTrackComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_sequence" MARKER="" POS2D="-0.006158 -0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_sequence.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_CINE" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/cinematics/${codenamelower}_cine.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_MainSequence" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/cinematics/${codenamelower}_mainsequence.tpl">
								<COMPONENTS NAME="MasterTape">
									<MasterTape />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_GRAPH" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/graph/${codenamelower}_graph.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="10.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="Camera_JD_Dummy" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_emptyactor.tpl" />
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_TML" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/timeline/${codenamelower}_tml.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_dance" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_karaoke" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_VIDEO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/videoscoach/${codenamelower}_video.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="-1.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="VideoScreen" MARKER="" POS2D="0.000000 -4.500000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_player_main.tpl">
								<COMPONENTS NAME="PleoComponent">
									<PleoComponent video="world/maps/${codenamelower}/videoscoach/${codenamelower}.webm" dashMPD="world/maps/${codenamelower}/videoscoach/${codenamelower}.mpd" channelID="" />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="3.941238 2.220000" xFLIPPED="0" USERFRIENDLY="VideoOutput" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_output_mainscene_main.tpl">
								<COMPONENTS NAME="PleoTextureGraphicComponent">
									<PleoTextureGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000" channelID="">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/pleofullscreen.msh" stencilTest="0" alphaTest="0" alphaRef="0">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</PleoTextureGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename} : Template Artist - Template Title&#10;JDVer = 5, ID = 842776738, Type = 1 (Flags 0x00000000), NbCoach = 2, Difficulty = 2" MARKER="" POS2D="-3.531976 -1.485322" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/songdesc.tpl">
				<COMPONENTS NAME="JD_SongDescComponent">
					<JD_SongDescComponent />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_menuart" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/menuart/${codenamelower}_menuart.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="3" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_2" MARKER="" POS2D="524.381104 670.829834" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_2.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_3" MARKER="" POS2D="524.381104 670.829834" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_3.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUTODANCE" MARKER="" POS2D="0.000000 -0.033823" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_autodance" MARKER="" POS2D="-0.006150 -0.003075" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.tpl">
								<COMPONENTS NAME="JD_AutodanceComponent">
									<JD_AutodanceComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0">
				<sceneConfigs NAME="JD_MapSceneConfig">
					<JD_MapSceneConfig name="" soundContext="" hud="0" phoneTitleLocId="4294967295" phoneImage="">
						<ENUM NAME="Pause_Level" SEL="6" />
						<ENUM NAME="type" SEL="1" />
						<ENUM NAME="musicscore" SEL="2" />
					</JD_MapSceneConfig>
				</sceneConfigs>
			</SceneConfigs>
		</sceneConfigs>
	</Scene>
</root>
`
}
if (coachcount == 4) {
	mainscene_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="2.000000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<PLATFORM_FILTER>
			<TargetFilterList platform="WII">
				<objects VAL="${codename}_AUTODANCE" />
			</TargetFilterList>
		</PLATFORM_FILTER>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUDIO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/audio/${codenamelower}_audio.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="MusicTrack" MARKER="" POS2D="1.125962 -0.418641" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_musictrack.tpl">
								<COMPONENTS NAME="MusicTrackComponent">
									<MusicTrackComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_sequence" MARKER="" POS2D="-0.006158 -0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/audio/${codenamelower}_sequence.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_CINE" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/cinematics/${codenamelower}_cine.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_MainSequence" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/cinematics/${codenamelower}_mainsequence.tpl">
								<COMPONENTS NAME="MasterTape">
									<MasterTape />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_GRAPH" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/graph/${codenamelower}_graph.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="10.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="Camera_JD_Dummy" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_emptyactor.tpl" />
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_TML" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/timeline/${codenamelower}_tml.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_dance" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000001" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_tml_karaoke" MARKER="" POS2D="-1.157740 0.006158" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.tpl">
								<COMPONENTS NAME="TapeCase_Component">
									<TapeCase_Component />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_VIDEO" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/videoscoach/${codenamelower}_video.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="-1.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="VideoScreen" MARKER="" POS2D="0.000000 -4.500000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_player_main.tpl">
								<COMPONENTS NAME="PleoComponent">
									<PleoComponent video="world/maps/${codenamelower}/videoscoach/${codenamelower}.webm" dashMPD="world/maps/${codenamelower}/videoscoach/${codenamelower}.mpd" channelID="" />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="3.941238 2.220000" xFLIPPED="0" USERFRIENDLY="VideoOutput" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/_common/videoscreen/video_output_mainscene_main.tpl">
								<COMPONENTS NAME="PleoTextureGraphicComponent">
									<PleoTextureGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000" channelID="">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/pleofullscreen.msh" stencilTest="0" alphaTest="0" alphaRef="0">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</PleoTextureGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename} : Template Artist - Template Title&#10;JDVer = 5, ID = 842776738, Type = 1 (Flags 0x00000000), NbCoach = 2, Difficulty = 2" MARKER="" POS2D="-3.531976 -1.485322" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/songdesc.tpl">
				<COMPONENTS NAME="JD_SongDescComponent">
					<JD_SongDescComponent />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_menuart" MARKER="" POS2D="0.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/menuart/${codenamelower}_menuart.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="3" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="1">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_generic" MARKER="" POS2D="266.087555 197.629959" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_generic.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_online" MARKER="" POS2D="-150.000000 0.000000" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_online.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumcoach" MARKER="" POS2D="738.106323 359.612030" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumcoach.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.300000 0.300000" xFLIPPED="0" USERFRIENDLY="${codename}_cover_albumbkg" MARKER="" POS2D="1067.972168 201.986328" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha_mul_b.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_cover_albumbkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="world/ui/textures/mask_square.tga" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_1" MARKER="" POS2D="212.784500 663.680176" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_1.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_2" MARKER="" POS2D="524.381104 670.829834" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_2.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_3" MARKER="" POS2D="524.381104 670.829834" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_3.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="0.290211 0.290211" xFLIPPED="0" USERFRIENDLY="${codename}_coach_4" MARKER="" POS2D="524.381104 670.829834" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="4294967295" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="6" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/ui/materials/alpha.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_coach_4.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="6" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="256.000000 128.000000" xFLIPPED="0" USERFRIENDLY="${codename}_banner_bkg" MARKER="" POS2D="1487.410156 -32.732918" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/tpl_materialgraphiccomponent2d.tpl">
								<COMPONENTS NAME="MaterialGraphicComponent">
									<MaterialGraphicComponent colorComputerTagId="0" renderInTarget="0" disableLight="0" disableShadow="1" AtlasIndex="0" customAnchor="0.000000 0.000000" SinusAmplitude="0.000000 0.000000 0.000000" SinusSpeed="1.000000" AngleX="0.000000" AngleY="0.000000">
										<PrimitiveParameters>
											<GFXPrimitiveParam colorFactor="1.000000 1.000000 1.000000 1.000000">
												<ENUM NAME="gfxOccludeInfo" SEL="0" />
											</GFXPrimitiveParam>
										</PrimitiveParameters>
										<ENUM NAME="anchor" SEL="1" />
										<material>
											<GFXMaterialSerializable ATL_Channel="0" ATL_Path="" shaderPath="world/_common/matshader/multitexture_1layer.msh" stencilTest="0" alphaTest="4294967295" alphaRef="4294967295">
												<textureSet>
													<GFXMaterialTexturePathSet diffuse="world/maps/${codenamelower}/menuart/textures/${codenamelower}_banner_bkg.tga" back_light="" normal="" separateAlpha="" diffuse_2="" back_light_2="" anim_impostor="" diffuse_3="" diffuse_4="" />
												</textureSet>
												<materialParams>
													<GFXMaterialSerializableParam Reflector_factor="0.000000" />
												</materialParams>
											</GFXMaterialSerializable>
										</material>
										<ENUM NAME="oldAnchor" SEL="1" />
									</MaterialGraphicComponent>
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<ACTORS NAME="SubSceneActor">
			<SubSceneActor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_AUTODANCE" MARKER="" POS2D="0.000000 -0.033823" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="enginedata/actortemplates/subscene.tpl" RELATIVEPATH="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.isc" EMBED_SCENE="1" IS_SINGLE_PIECE="0" ZFORCED="1" DIRECT_PICKING="1" IGNORE_SAVE="0">
				<ENUM NAME="viewType" SEL="2" />
				<SCENE>
					<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
						<ACTORS NAME="Actor">
							<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_autodance" MARKER="" POS2D="-0.006150 -0.003075" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.tpl">
								<COMPONENTS NAME="JD_AutodanceComponent">
									<JD_AutodanceComponent />
								</COMPONENTS>
							</Actor>
						</ACTORS>
						<sceneConfigs>
							<SceneConfigs activeSceneConfig="0" />
						</sceneConfigs>
					</Scene>
				</SCENE>
			</SubSceneActor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0">
				<sceneConfigs NAME="JD_MapSceneConfig">
					<JD_MapSceneConfig name="" soundContext="" hud="0" phoneTitleLocId="4294967295" phoneImage="">
						<ENUM NAME="Pause_Level" SEL="6" />
						<ENUM NAME="type" SEL="1" />
						<ENUM NAME="musicscore" SEL="2" />
					</JD_MapSceneConfig>
				</sceneConfigs>
			</SceneConfigs>
		</sceneConfigs>
	</Scene>
</root>
`
}
fs.writeFileSync(cachePath + "/" + codenamelower + "_main_scene.isc.ckd", mainscene_isc, function(err) {
    console.log(err)
});

var mainscene_sgs = `S{"settings":{"__class":"JD_MapSceneConfig","Pause_Level":6,"name":"","type":1,"musicscore":2,"soundContext":"","hud":0,"phoneTitleLocId":4294967295,"phoneImage":""}} `

fs.writeFileSync(cachePath + "/" + codenamelower + "_main_scene.sgs.ckd", mainscene_sgs, function(err) {
    console.log(err)
});

var autodance_tpl = `{"__class":"Actor_Template","WIP":0,"LOWUPDATE":0,"UPDATE_LAYER":0,"PROCEDURAL":0,"STARTPAUSED":0,"FORCEISENVIRONMENT":0,"COMPONENTS":[{"__class":"JD_AutodanceComponent_Template","song":"${codename}","autodanceData":{"__class":"JD_AutodanceData","recording_structure":{"__class":"JD_AutodanceRecordingStructure","records":[{"__class":"Record","Start":88,"Duration":16},{"__class":"Record","Start":136,"Duration":8},{"__class":"Record","Start":188,"Duration":8},{"__class":"Record","Start":252,"Duration":16}]},"video_structure":{"__class":"JD_AutodanceVideoStructure","SongStartPosition":244,"Duration":32,"ThumbnailTime":0,"FadeOutDuration":3,"GroundPlanePath":"invalid ","FirstLayerTripleBackgroundPath":"invalid ","SecondLayerTripleBackgroundPath":"invalid ","ThirdLayerTripleBackgroundPath":"invalid ","playback_events":[{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":0,"StartTime":244,"Duration":1,"Speed":1},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":0,"StartTime":245,"Duration":1,"Speed":1},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":0,"StartTime":246,"Duration":1,"Speed":1},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":0,"StartTime":247,"Duration":1,"Speed":1},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":3,"StartTime":248,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":3,"StartTime":248.500000,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":3,"StartTime":249,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":3,"StartTime":249.500000,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":1,"StartClip":0,"StartTime":250,"Duration":1,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":1,"StartClip":1,"StartTime":251,"Duration":1,"Speed":4},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":5,"StartTime":252,"Duration":1,"Speed":1.500000},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":5,"StartTime":253,"Duration":1,"Speed":1.500000},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":6,"StartTime":254,"Duration":2,"Speed":1.800000},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":6,"StartTime":256,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":6,"StartTime":256.500000,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":6,"StartTime":257,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":6,"StartTime":257.500000,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":6,"StartTime":258,"Duration":0.500000,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":7,"StartTime":258.500000,"Duration":1.500000,"Speed":1.500000},{"__class":"PlaybackEvent","ClipNumber":2,"StartClip":0,"StartTime":260,"Duration":1,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":1,"StartClip":2,"StartTime":261,"Duration":1,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":1,"StartClip":2,"StartTime":262,"Duration":1,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":1,"StartClip":2,"StartTime":263,"Duration":1,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":3,"StartClip":0,"StartTime":264,"Duration":1.500000,"Speed":3},{"__class":"PlaybackEvent","ClipNumber":3,"StartClip":3,"StartTime":265.500000,"Duration":1.500000,"Speed":-3},{"__class":"PlaybackEvent","ClipNumber":3,"StartClip":1.500000,"StartTime":267,"Duration":1,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":3,"StartClip":2.200000,"StartTime":268,"Duration":1,"Speed":3},{"__class":"PlaybackEvent","ClipNumber":2,"StartClip":0,"StartTime":269,"Duration":2,"Speed":3},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":0,"StartTime":271,"Duration":1,"Speed":1},{"__class":"PlaybackEvent","ClipNumber":3,"StartClip":4,"StartTime":272,"Duration":2,"Speed":2},{"__class":"PlaybackEvent","ClipNumber":0,"StartClip":0,"StartTime":274,"Duration":1,"Speed":1},{"__class":"PlaybackEvent","ClipNumber":3,"StartClip":3,"StartTime":275,"Duration":1,"Speed":5}],"background_effect":{"__class":"AutoDanceFxDesc","Opacity":1,"ColorLow":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"ColorMid":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"ColorHigh":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"LowToMid":0.333000,"LowToMidWidth":0.150000,"MidToHigh":0.666000,"MidToHighWidth":0.150000,"SobColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"OutColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":0},"ThickMiddle":0.400000,"ThickInner":0.100000,"ThickSmooth":0.100000,"ShvNbFrames":0,"PartsScale":[0,0,0,0,0],"HalftoneFactor":0,"HalftoneCutoutLevels":256,"UVBlackoutFactor":0,"UVBlackoutDesaturation":0.200000,"UVBlackoutContrast":4,"UVBlackoutBrightness":0,"UVBlackoutColor":{"__class":"GFX_Vector4","x":0.549020,"y":0.549020,"z":1,"w":1},"ToonFactor":0,"ToonCutoutLevels":8,"RefractionFactor":0,"RefractionTint":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"RefractionScale":{"__class":"GFX_Vector4","x":0.030000,"y":0.030000,"z":0.030000,"w":0.030000},"RefractionOpacity":0.200000,"ColoredShivaThresholds":{"__class":"GFX_Vector4","x":0.100000,"y":0.300000,"z":0.600000,"w":0.950000},"ColoredShivaColor0":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"ColoredShivaColor1":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"ColoredShivaColor2":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"SaturationModifier":0,"SlimeFactor":0,"SlimeColor":{"__class":"GFX_Vector4","x":0.499020,"y":0.629176,"z":0.136039,"w":1},"SlimeOpacity":0.200000,"SlimeAmbient":0.200000,"SlimeNormalTiling":7,"SlimeLightAngle":0,"SlimeRefraction":0.091300,"SlimeRefractionIndex":1.083700,"SlimeSpecular":1,"SlimeSpecularPower":10,"OverlayBlendFactor":0,"OverlayBlendColor":{"__class":"GFX_Vector4","x":0.721569,"y":0.639216,"z":0.756863,"w":1},"BackgroundSobelFactor":0,"BackgroundSobelColor":{"__class":"GFX_Vector4","x":0,"y":1,"z":1,"w":1},"PlayerGlowFactor":0,"PlayerGlowColor":{"__class":"GFX_Vector4","x":0,"y":1,"z":1,"w":1},"SwapHeadWithPlayer":[0,1,2,3,4,5],"AnimatePlayerHead":[0,0,0,0,0,0],"AnimatedHeadTotalTime":20,"AnimatedHeadRestTime":16,"AnimatedHeadFrameTime":0.600000,"AnimatedHeadMaxDistance":1.250000,"AnimatedHeadMaxAngle":1.200000,"ScreenBlendInverseAlphaFactor":0,"ScreenBlendInverseAlphaScaleX":0,"ScreenBlendInverseAlphaScaleY":0,"ScreenBlendInverseAlphaTransX":0,"ScreenBlendInverseAlphaTransY":0,"TintMulColorFactor":0,"TintMulColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"FloorPlaneFactor":0,"FloorPlaneTiles":{"__class":"GFX_Vector4","x":8,"y":8,"z":0,"w":0},"FloorSpeedX":0,"FloorSpeedY":0,"FloorWaveSpeed":0,"FloorBlendMode":0,"FloorPlaneImageID":0,"StartRadius":3,"EndRadius":2,"RadiusVariance":0.500000,"RadiusNoiseRate":0,"RadiusNoiseAmp":0,"MinSpin":-4,"MaxSpin":4,"DirAngle":0,"MinWanderRate":2,"MaxWanderRate":3,"MinWanderAmp":0.100000,"MaxWanderAmp":0.200000,"MinSpeed":0.200000,"MaxSpeed":0.400000,"MotionPower":1.500000,"Amount":0,"ImageID":7,"StartR":1,"StartG":0.100000,"StartB":0.100000,"EndR":0.100000,"EndG":0.200000,"EndB":1,"StartAlpha":1,"EndAlpha":1,"TexturedOutlineFactor":0,"TexturedOutlineTiling":1,"TripleLayerBackgroundFactor":0,"TripleLayerBackgroundTintColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":0},"TripleLayerBackgroundSpeedX":0,"TripleLayerBackgroundSpeedY":0,"TrailEffectId":0},"player_effect":{"__class":"AutoDanceFxDesc","Opacity":1,"ColorLow":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"ColorMid":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"ColorHigh":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"LowToMid":0.333000,"LowToMidWidth":0.150000,"MidToHigh":0.666000,"MidToHighWidth":0.150000,"SobColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"OutColor":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":0},"ThickMiddle":0.400000,"ThickInner":0.100000,"ThickSmooth":0.100000,"ShvNbFrames":0,"PartsScale":[0,0,0,0,0],"HalftoneFactor":0,"HalftoneCutoutLevels":256,"UVBlackoutFactor":0,"UVBlackoutDesaturation":0.200000,"UVBlackoutContrast":4,"UVBlackoutBrightness":0,"UVBlackoutColor":{"__class":"GFX_Vector4","x":0.549020,"y":0.549020,"z":1,"w":1},"ToonFactor":0,"ToonCutoutLevels":256,"RefractionFactor":0,"RefractionTint":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"RefractionScale":{"__class":"GFX_Vector4","x":0.030000,"y":0.030000,"z":0.030000,"w":0.030000},"RefractionOpacity":0.200000,"ColoredShivaThresholds":{"__class":"GFX_Vector4","x":0.100000,"y":0.300000,"z":0.600000,"w":0.950000},"ColoredShivaColor0":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"ColoredShivaColor1":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"ColoredShivaColor2":{"__class":"GFX_Vector4","x":1,"y":1,"z":1,"w":1},"SaturationModifier":0,"SlimeFactor":0,"SlimeColor":{"__class":"GFX_Vector4","x":0.894118,"y":0.294118,"z":1,"w":0.549020},"SlimeOpacity":0.200000,"SlimeAmbient":0.200000,"SlimeNormalTiling":7,"SlimeLightAngle":0,"SlimeRefraction":0.100000,"SlimeRefractionIndex":1.100000,"SlimeSpecular":1.100000,"SlimeSpecularPower":2,"OverlayBlendFactor":0,"OverlayBlendColor":{"__class":"GFX_Vector4","x":0.721569,"y":0.639216,"z":0.756863,"w":1},"BackgroundSobelFactor":0,"BackgroundSobelColor":{"__class":"GFX_Vector4","x":0,"y":1,"z":1,"w":1},"PlayerGlowFactor":0,"PlayerGlowColor":{"__class":"GFX_Vector4","x":0,"y":1,"z":1,"w":1},"SwapHeadWithPlayer":[0,1,2,3,4,5],"AnimatePlayerHead":[0,0,0,0,0,0],"AnimatedHeadTotalTime":20,"AnimatedHeadRestTime":16,"AnimatedHeadFrameTime":0.600000,"AnimatedHeadMaxDistance":1.250000,"AnimatedHeadMaxAngle":1.200000,"ScreenBlendInverseAlphaFactor":0,"ScreenBlendInverseAlphaScaleX":0,"ScreenBlendInverseAlphaScaleY":0,"ScreenBlendInverseAlphaTransX":0,"ScreenBlendInverseAlphaTransY":0,"TintMulColorFactor":0,"TintMulColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":1},"FloorPlaneFactor":0,"FloorPlaneTiles":{"__class":"GFX_Vector4","x":8,"y":8,"z":0,"w":0},"FloorSpeedX":0,"FloorSpeedY":0,"FloorWaveSpeed":0,"FloorBlendMode":0,"FloorPlaneImageID":0,"StartRadius":0,"EndRadius":2,"RadiusVariance":0,"RadiusNoiseRate":0,"RadiusNoiseAmp":0,"MinSpin":0,"MaxSpin":0,"DirAngle":0,"MinWanderRate":0,"MaxWanderRate":0,"MinWanderAmp":0,"MaxWanderAmp":0,"MinSpeed":2,"MaxSpeed":4,"MotionPower":1,"Amount":0,"ImageID":0,"StartR":0,"StartG":0,"StartB":0,"EndR":1,"EndG":1,"EndB":1,"StartAlpha":1,"EndAlpha":1,"TexturedOutlineFactor":0,"TexturedOutlineTiling":0,"TripleLayerBackgroundFactor":0,"TripleLayerBackgroundTintColor":{"__class":"GFX_Vector4","x":0,"y":0,"z":0,"w":0},"TripleLayerBackgroundSpeedX":0,"TripleLayerBackgroundSpeedY":0,"TrailEffectId":0}},"autodanceSoundPath":"world/maps/${codenamelower}/autodance/${codenamelower}.ogg"}}]} `

fs.writeFileSync(cachePath + "/autodance/" + codenamelower + "_autodance.tpl.ckd", autodance_tpl, function(err) {
    console.log(err)
});

var autodance_isc = `<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
	<Scene ENGINE_VERSION="253653" GRIDUNIT="0.500000" DEPTH_SEPARATOR="0" NEAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" FAR_SEPARATOR="1.000000 0.000000 0.000000 0.000000, 0.000000 1.000000 0.000000 0.000000, 0.000000 0.000000 1.000000 0.000000, 0.000000 0.000000 0.000000 1.000000" viewFamily="0">
		<ACTORS NAME="Actor">
			<Actor RELATIVEZ="0.000000" SCALE="1.000000 1.000000" xFLIPPED="0" USERFRIENDLY="${codename}_autodance" MARKER="" POS2D="-0.006150 -0.003075" ANGLE="0.000000" INSTANCEDATAFILE="" LUA="world/maps/${codenamelower}/autodance/${codenamelower}_autodance.tpl">
				<COMPONENTS NAME="JD_AutodanceComponent">
					<JD_AutodanceComponent />
				</COMPONENTS>
			</Actor>
		</ACTORS>
		<sceneConfigs>
			<SceneConfigs activeSceneConfig="0" />
		</sceneConfigs>
	</Scene>
</root>
`

fs.writeFileSync(cachePath + "/autodance/" + codenamelower + "_autodance.isc.ckd", autodance_isc, function(err) {
    console.log(err)
});

const codelength_hex = getHex(codename.length.toString(16))
const codename_hex = Buffer.from(codename, "utf8").toString("hex")
const path_hex = Buffer.from(`world/maps/${codenamelower}/`, "utf8").toString("hex")
const pathlength_hex = getHex((`world/maps/${codenamelower}/`).length.toString(16))

function generateHexLength(string) {
	return getHex((string).length.toString(16))
}

function generateHexString(string) {
	return Buffer.from(string, "utf8").toString("hex")
}

var autodance_act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF00000000" + generateHexLength(`${codenamelower}_autodance.tpl`) + generateHexString(`${codenamelower}_autodance.tpl`) + generateHexLength(`world/maps/${codenamelower}/autodance/`) + generateHexString(`world/maps/${codenamelower}/autodance/`) + "1019CF8E00000000000000000000000167B8BB77"

fs.writeFileSync(cachePath + "/autodance/" + codenamelower + "_autodance.act.ckd", Buffer.from(autodance_act, "hex"), function(err) {
    console.log(err)
});

var mainsequence_act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF00000000" + generateHexLength(`${codenamelower}_mainsequence.tpl`) + generateHexString(`${codenamelower}_mainsequence.tpl`) + generateHexLength(`world/maps/${codenamelower}/cinematics/`) + generateHexString(`world/maps/${codenamelower}/cinematics/`) + "806F57AB000000000000000000000001677B269B"


fs.writeFileSync(cachePath + "/cinematics/" + codenamelower + "_mainsequence.act.ckd", Buffer.from(mainsequence_act, "hex"), function(err) {
    console.log(err)
});

var mainsequence_act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF00000000" + generateHexLength(`${codenamelower}_mainsequence.tpl`) + generateHexString(`${codenamelower}_mainsequence.tpl`) + generateHexLength(`world/maps/${codenamelower}/cinematics/`) + generateHexString(`world/maps/${codenamelower}/cinematics/`) + "806F57AB000000000000000000000001677B269B"

var coach1act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000060000000000000000" + generateHexLength(`${codenamelower}_coach_1.tga`) + generateHexString(`${codenamelower}_coach_1.tga`) + generateHexLength(`world/maps/${codenamelower}/menuart/textures/`) + generateHexString(`world/maps/${codenamelower}/menuart/textures/`) + "A0CC7365000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

var coach2act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000060000000000000000" + generateHexLength(`${codenamelower}_coach_2.tga`) + generateHexString(`${codenamelower}_coach_2.tga`) + generateHexLength(`world/maps/${codenamelower}/menuart/textures/`) + generateHexString(`world/maps/${codenamelower}/menuart/textures/`) + "EECC7365000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

var coach3act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000060000000000000000" + generateHexLength(`${codenamelower}_coach_3.tga`) + generateHexString(`${codenamelower}_coach_3.tga`) + generateHexLength(`world/maps/${codenamelower}/menuart/textures/`) + generateHexString(`world/maps/${codenamelower}/menuart/textures/`) + "EACC7365000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

var coach4act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000060000000000000000" + generateHexLength(`${codenamelower}_coach_4.tga`) + generateHexString(`${codenamelower}_coach_4.tga`) + generateHexLength(`world/maps/${codenamelower}/menuart/textures/`) + generateHexString(`world/maps/${codenamelower}/menuart/textures/`) + "A1CC7365000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

if (coachcount === 1) {
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_1.act.ckd", Buffer.from(coach1act, "hex"), function(err) {
    console.log(err)
});
}
if (coachcount === 2) {
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_1.act.ckd", Buffer.from(coach1act, "hex"), function(err) {
    console.log(err)
});
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_2.act.ckd", Buffer.from(coach2act, "hex"), function(err) {
    console.log(err)
});
}
if (coachcount === 3) {
		fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_1.act.ckd", Buffer.from(coach1act, "hex"), function(err) {
    console.log(err)
});
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_2.act.ckd", Buffer.from(coach2act, "hex"), function(err) {
    console.log(err)
});
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_3.act.ckd", Buffer.from(coach3act, "hex"), function(err) {
    console.log(err)
});
}
if (coachcount === 4) {
		fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_1.act.ckd", Buffer.from(coach1act, "hex"), function(err) {
    console.log(err)
});
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_2.act.ckd", Buffer.from(coach2act, "hex"), function(err) {
    console.log(err)
});
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_3.act.ckd", Buffer.from(coach3act, "hex"), function(err) {
    console.log(err)
});
	fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_coach_4.act.ckd", Buffer.from(coach4act, "hex"), function(err) {
    console.log(err)
});
}

var banneract = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000010000000000000000"+generateHexLength(`${codenamelower}_banner_bkg.tga`)+generateHexString(`${codenamelower}_banner_bkg.tga`)+generateHexLength(`world/maps/${codenamelower}/menuart/textures/`)+generateHexString(`world/maps/${codenamelower}/menuart/textures/`)+"9FF68EF0000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_banner_bkg.act.ckd", Buffer.from(banneract, "hex"), function(err) {
    console.log(err)
});

var albumbkgact = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000010000000000000000"+generateHexLength(`${codenamelower}_cover_albumbkg.tga`)+generateHexString(`${codenamelower}_cover_albumbkg.tga`)+generateHexLength(`world/maps/${codenamelower}/menuart/textures/`)+generateHexString(`world/maps/${codenamelower}/menuart/textures/`)+"A8105B4D000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_cover_albumbkg.act.ckd", Buffer.from(albumbkgact, "hex"), function(err) {
    console.log(err)
});

var albumcoachact = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000060000000000000000"+generateHexLength(`${codenamelower}_cover_albumcoach.tga`)+generateHexString(`${codenamelower}_cover_albumcoach.tga`)+generateHexLength(`world/maps/${codenamelower}/menuart/textures/`)+generateHexString(`world/maps/${codenamelower}/menuart/textures/`)+"20B3BFBD000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF0000000000000009616C7068612E6D736800000013776F726C642F75692F6D6174657269616C732FD2854E00000000000000000000000000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_cover_albumcoach.act.ckd", Buffer.from(albumcoachact, "hex"), function(err) {
    console.log(err)
});

var genericact = "00000001000000003F8000003F800000000000000000000000000000000000010000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000010000000000000000"+generateHexLength(`${codenamelower}_cover_generic.tga`)+generateHexString(`${codenamelower}_cover_generic.tga`)+generateHexLength(`world/maps/${codenamelower}/menuart/textures/`)+generateHexString(`world/maps/${codenamelower}/menuart/textures/`) + "D991FA0D000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000000000000000000000000000000000000000000000000000000000003F800000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_cover_generic.act.ckd", Buffer.from(genericact, "hex"), function(err) {
    console.log(err)
});

var onlineact = "00000001000000003F8000003F800000000000000000000000000000000000010000000000000000000000000000000000000000FFFFFFFF000000000000002274706C5F6D6174657269616C67726170686963636F6D706F6E656E7432642E74706C0000001A656E67696E65646174612F6163746F7274656D706C617465732FB4A817A800000000000000000000000172B61FC53F8000003F8000003F8000003F80000000000000000000000000000000000000FFFFFFFF00000000000000010000000000000000"+generateHexLength(`${codenamelower}_cover_online.tga`)+generateHexString(`${codenamelower}_cover_online.tga`)+generateHexLength(`world/maps/${codenamelower}/menuart/textures/`)+generateHexString(`world/maps/${codenamelower}/menuart/textures/`) + "E491FA0D000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF000000000000000000000000FFFFFFFF00000000000000000000000000000000FFFFFFFF00000000000000176D756C7469746578747572655F316C617965722E6D736800000018776F726C642F5F636F6D6D6F6E2F6D61747368616465722FD7E7D9C7000000000000000000000000000000000000000000000000000000000000000000000000000000003F800000FFFFFFFFFFFFFFFF0000000000000000000000003F800000000000000000000000000001"

fs.writeFileSync(cachePath + "/menuart/actors/" + codenamelower + "_cover_online.act.ckd", Buffer.from(onlineact, "hex"), function(err) {
    console.log(err)
});

var dance_act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF00000000"+generateHexLength(`${codenamelower}_tml_dance.tpl`)+generateHexString(`${codenamelower}_tml_dance.tpl`)+generateHexLength(`world/maps/${codenamelower}/timeline/`)+generateHexString(`world/maps/${codenamelower}/timeline/`)+"8FCBDA63000000000000000000000001231F27DE"

fs.writeFileSync(cachePath + "/timeline/" + codenamelower + "_tml_dance.act.ckd", Buffer.from(dance_act, "hex"), function(err) {
    console.log(err)
});

var karaoke_act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF00000000"+generateHexLength(`${codenamelower}_tml_karaoke.tpl`)+generateHexString(`${codenamelower}_tml_karaoke.tpl`)+generateHexLength(`world/maps/${codenamelower}/timeline/`)+generateHexString(`world/maps/${codenamelower}/timeline/`)+"AFBEDA63000000000000000000000001231F27DE"

fs.writeFileSync(cachePath + "/timeline/" + codenamelower + "_tml_karaoke.act.ckd", Buffer.from(karaoke_act, "hex"), function(err) {
    console.log(err)
});

var video_player_main_act = "00000001000000003F8000003F8000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF0000000000000015766964656F5F706C617965725F6D61696E2E74706C0000001A776F726C642F5F636F6D6D6F6E2F766964656F73637265656E2FF5D5E8F20000000000000000000000011263DAD9"+generateHexLength(`${codenamelower}.webm`)+generateHexString(`${codenamelower}.webm`)+generateHexLength(`world/maps/${codenamelower}/videoscoach/`)+generateHexString(`world/maps/${codenamelower}/videoscoach/`)+"8F3F298600000000"+generateHexLength(`${codenamelower}.mpd`)+generateHexString(`${codenamelower}.mpd`)+generateHexLength(`world/maps/${codenamelower}/videoscoach/`)+generateHexString(`world/maps/${codenamelower}/videoscoach/`)+"4312021B0000000000000000"

fs.writeFileSync(cachePath + "/videoscoach/video_player_main.act.ckd", Buffer.from(video_player_main_act, "hex"), function(err) {
    console.log(err)
});

var mpd = "0000000100432947AE3F800000000000010000000000000000432947AE00000001000000000000000A766964656F2F7765626D00000003767038000004C0000002D000000000000000010101000000040000000000073964"+generateHexLength(`jmcs://jd-contents/${codename}/${codename}_LOW.webm`)+generateHexString(`jmcs://jd-contents/${codename}/${codename}_LOW.webm`)+"000000000000024B0000024B00000D5B00000001001C760E"+generateHexLength(`jmcs://jd-contents/${codename}/${codename}_MID.webm`)+generateHexString(`jmcs://jd-contents/${codename}/${codename}_MID.webm`)+"000000000000024B0000024B00000DBF000000020038FF8E"+generateHexLength(`jmcs://jd-contents/${codename}/${codename}_HIGH.webm`)+generateHexString(`jmcs://jd-contents/${codename}/${codename}_HIGH.webm`)+"000000000000024B0000024B00000DE1000000030070946D"+generateHexLength(`jmcs://jd-contents/${codename}/${codename}_ULTRA.webm`)+generateHexString(`jmcs://jd-contents/${codename}/${codename}_ULTRA.webm`)+"000000000000024B0000024B00000DF2"

fs.writeFileSync(cachePath + "/videoscoach/" + codenamelower + ".mpd.ckd", Buffer.from(mpd, "hex"), function(err) {
    console.log(err)

});

var songdesc_act = "00000001000000003F8000003F800000000000000000000000000000000000010000000000000000000000000000000000000000FFFFFFFF000000000000000C736F6E67646573632E74706C"+generateHexLength(`world/maps/${codenamelower}/`)+generateHexString(`world/maps/${codenamelower}/`)+"A006695E000000000000000000000001E07FCC3F"

fs.writeFileSync(cachePath + "/songdesc.act.ckd", Buffer.from(songdesc_act, "hex"), function(err) {
    console.log(err)
});

const msmCount = fs.readdirSync(`./input/${codename}/moves/`)

msmCount.forEach(files => {
	fs.copyFileSync(`./input/${codename}/moves/` + files, `./output_mainscene/${codename}/world/maps/${codenamelower}/timeline/moves/wiiu/` + files)
})

const pictoCount = fs.readdirSync(`./input/${codename}/pictos/`)

pictoCount.forEach(files => {
	fs.copyFileSync(`./input/${codename}/pictos/` + files, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/timeline/pictos/` + files)
})

const texturesCount = fs.readdirSync(`./input/${codename}/textures/`)

texturesCount.forEach(files => {
	fs.copyFileSync(`./input/${codename}/textures/` + files, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/menuart/textures/` + files)
})

fs.copyFileSync(`./input/${codename}/${codenamelower}_tml_dance.dtape.ckd`, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/timeline/${codenamelower}_tml_dance.dtape.ckd`)

fs.copyFileSync(`./input/${codename}/${codenamelower}_tml_karaoke.ktape.ckd`, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/timeline/${codenamelower}_tml_karaoke.ktape.ckd`)

fs.copyFileSync(`./input/${codename}/${codenamelower}_musictrack.tpl.ckd`, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/audio/${codenamelower}_musictrack.tpl.ckd`)

fs.copyFileSync(`./input/${codename}/songdesc.tpl.ckd`, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/songdesc.tpl.ckd`)

if (fs.existsSync(`./input/${codename}/${codenamelower}.wav.ckd`)) {
fs.copyFileSync(`./input/${codename}/${codenamelower}.wav.ckd`, `./output_mainscene/${codename}/cache/itf_cooked/${platform}/world/maps/${codenamelower}/audio/${codenamelower}.wav.ckd`)
} else {}

if (fs.existsSync(`./input/${codename}/${codenamelower}.webm`)) {
	fs.copyFileSync(`./input/${codename}/${codenamelower}.webm`, `./output_mainscene/${codename}/world/maps/${codenamelower}/videoscoach/${codenamelower}.webm`)
} else {}

var songDesc = JSON.parse(fs.readFileSync(`./input/${codename}/songdesc.tpl.ckd`))
console.log(" ")
console.log("Generated mainscene!")
console.log(" ")
console.log("JDVersion: " + songDesc.COMPONENTS[0].JDVersion)
console.log("OriginalJDVersion: " + songDesc.COMPONENTS[0].OriginalJDVersion)
console.log("Title: " + songDesc.COMPONENTS[0].Title)
console.log("Artist: " + songDesc.COMPONENTS[0].Artist)
console.log("NumCoach: " + songDesc.COMPONENTS[0].NumCoach)