# ModTranslationHelper

[RU](README.md) | EN | [CN](README.zh.md)

Performed with:\
**Python 3.10, PyQt5, deep-translator**

### Contact the author, bug report, advise your wishes: [Discord Server](https://discord.gg/zcAbHfUSCt)

Program to help translate mods for Paradox Interactive games

Synopsis:\
The program was created to help localize mods for games from Paradox Interactive studio, but can be used to process any data stored in key format "value" in .yml and .txt files.

### To work it is necessary to:
- >Find the location where the game for which you intend to translate is installed. The default path for Crusader Kings 3 is to the localization folder (where the English, Russian, French, etc. folders are located):\
**../Steam/steamapps/common/Crusader Kings III/game/localization\.

- >Select the folder where the localization is stored (example: **../Steam/steamapps/workshop/content/1158310/2507209632/localization**).

- >You should choose the directory with the previous version of the translation if you are updating the translation and you already have a previous version of the translation. The program will search the old files and use the already translated strings to build the new version.

- >The translation directory is the folder where all the files created as a result of the work of the program will be placed.

### Additional features:
- >If you select the "Add machine translation" option, the machine translation of each line of the localization of all the files that you check in the box below will be added to the final files.
**Attention!** In this case you will not be able to use the files output by the program at once, the machine translation will be added immediately after the original string and will not be hidden from the player!

