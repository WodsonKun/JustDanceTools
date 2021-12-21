py bin\pictocutter_atlas.py

set ddsvar=%cd%\output_dds
for /R %%f IN (output_png\*.png) DO bin\nvcompress -bc3 "%%f" "%ddsvar%\%%~nf.dds"

set tgavar=%cd%\output_tgackd
for /R %%f IN (output_dds\*.dds) DO bin\quickbms -o "bin\scriptDDStoCKD.bms" "%%f" "%tgavar%"

pause