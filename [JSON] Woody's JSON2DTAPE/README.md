# Woody's JSON2DTAPE
A tool made to convert **Just Dance Now** / **Just Dance: Vitality School** JSONs in order to make them compatible with UbiArt Framework-based Just Dance games

## Requirements
- Python 3+
- [NVidia Texture Tools](https://github.com/castano/nvidia-texture-tools/releases)
- [QuickBMS](http://aluigi.altervista.org/quickbms.htm)

You also need a few Python modules, but you can all install all of them by using ``pip install -r requirements.txt`` from the tool folder

## How to use
- Place ``nvcompress.exe``, ``nvtt.dll``, ``nvtt.pdb`` and ``quickbms.exe`` on the ``bin`` folder
- Run ``woody_j2d.py``

## Credits
[augustodoidin · GitHub](https://github.com/augustodoidin/) | Beat Generator

[JDEliot · GitHub](https://github.com/JDEliot/) | Pictocutters (for both atlas and sprite), also helped on refactoring pieces of code

[planedec50 · YouTube](https://www.youtube.com/c/planedec50) | Interpolation method 

[castano · GitHub](https://github.com/castano/) | NVidia Texture Tools

[pinyin_jyutping_sentence · PyPI](https://pypi.org/project/pinyin_jyutping_sentence/) | Library used to convert Vitality School lyrics to Pinyin

[Unidecode · PyPI](https://pypi.org/project/Unidecode/) | Removes accents from Pinyin stuff

[numpy · PyPI](https://pypi.org/project/numpy/) | Interpolation method 

[Pillow · PyPI](https://pypi.org/project/Pillow/) | Image handling for pictocutting
