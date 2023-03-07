# ModTranslationHelper
## RU:

Выполнено с помощью:\
**Python 3.10, PyQt5, deep-translator**

### Связь с автором, отправить баг-репорт, сообщить свои пожелания: [Discord Server](https://discord.gg/zcAbHfUSCt)

Программа для помощи в переводах модов к играм Paradox Interactive

Справка:\
Программа создана для помощи в локализации модов для игр от студии Paradox Interactive, но может использоваться для обработки любых данных, хранящихся в формате ключ "значение" в файлах с расширением .yml и .txt.

### Для работы необходимо:
- >Найти место, где установлена игра, для которой вы собираетесь переводить. Путь обязательно должен вести к папке с локализацией(там где находятся папки english, russian, french и т.д.) 
Стандартный путь для Crusader Kings 3:\
**../Steam/steamapps/common/Crusader Kings III/game/localization**\
- >Указать папку, где хранится локализация мода (Пример: **../Steam/steamapps/workshop/content/1158310/2507209632/localization**)
- >Если происходит обновление перевода и у вас уже есть готовый перевод предыдущей версии, то стоит указать директорию с предыдущей версией перевода. Программа сама пробежится по старым файлам и использует уже переведенные строки для построения новой версии.
- >Директория перевода - это папка, в которую будут помещены все файлы, созданные в результате работы программы.

### Дополнительные функции:
- >Если отметить галочкой пункт "Добавить машинный перевод", то в финальные файлы будет добавлен машинный перевод каждой строки локализации всех файлов, которые вы отметите в поле ниже.\
**Внимание!** В таком случае использовать выданные программой файлы сразу нельзя, машинный перевод будет добавлен сразу после оригинальной строки и не будет скрыт от игрока!

## EN:

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

