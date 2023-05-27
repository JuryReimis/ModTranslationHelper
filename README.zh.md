# ModTranslationHelper

RU(README.md) | [EN](README.en.md) | CN

运行环境:\
**Python 3.10, PyQt5, deep-translator**

### 联系作者，报告错误，反馈需求: [Discord Server](https://discord.gg/zcAbHfUSCt)

帮助翻译Paradox Interactive游戏的MOD的程序

简介:\
这个程序是为了帮助Paradox Interactive studio的游戏mods进行本地化，但也可以用来处理任何以key格式 "value "存储在.yml和.txt文件的数据。

### 准备工作
- >找到你打算翻译的游戏的安装位置。《十字军之王3》的默认路径是本地化文件夹（英语、俄语、法语等文件夹的位置）：\
**../Steam/steamapps/common/Crusader Kings III/game/localization\.

- >选择存储本地化的文件夹 (举个例子: **../Steam/steamapps/workshop/content/1158310/2507209632/localization**).

- >如果你要更新翻译，而你已经有了以前的翻译版本，你应该选择有以前的翻译版本的目录。该程序将搜索旧文件，并使用已经翻译好的字符串来建立新版本。

- >翻译目录是放置所有因程序工作而创建的文件的文件夹。

### 附加功能
- >如果你选择了 "添加机器翻译 "选项，那么你在下面方框中勾选的所有文件的本地化的每一行的机器翻译将被添加到最终文件中。\
**注意!** 在这种情况下，你将不能一次性使用程序输出的文件，机器翻译将被立即添加到原始字符串之后，并且不会被隐藏在播放器中!

