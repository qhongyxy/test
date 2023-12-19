# [VM虚拟机安装：](https://github.com/CCNU-IOT/CCNU-IOT-DOCS/blob/hardware-group/Linux/虚拟机安装.md#vm虚拟机安装)

第一节引用了姜学长的教程

第二节是Ubuntu22.04的clash安装及配置





## [1. 准备工作：](https://github.com/CCNU-IOT/CCNU-IOT-DOCS/blob/hardware-group/Linux/虚拟机安装.md#1-准备工作)

- 目前装虚拟机的文章满天🐦都是，之前协会这边也写过装虚拟机的文章，但当时写的也是比较稚嫩👶，现在再读感觉有很多不妥之处，会误导大家，因此重新写一份虚拟机安装教程⭐。

#### [1.1 理清思路：](https://github.com/CCNU-IOT/CCNU-IOT-DOCS/blob/hardware-group/Linux/虚拟机安装.md#11-理清思路)

- 我们这里要做的事情是装

  虚拟机

  ，什么是

  虚拟机

  呢？

  - Wikipedia🦁

    ：

    - **虚拟机**(virtual machine)，在计算机科学中的体系结构里，是指一种特殊的软件，可以在**计算机平台**和**用户**之间建立一种"**环境**"🐧，而用户则是基于虚拟机这个软件所建立的"环境"来操作**其它软件**。

  - 我的理解

    ：🤔

    - 上述所说的"环境"指的就是操作系统，而虚拟机就是运行这个操作系统的平台。

      - 我们可以理解为

        套娃行动

        ：

        - 用户本地的**硬件计算机**运行**Windows操作系统💯**(这里以Windows为例)。
        - **Windows操作系统**中的一个**软件**(虚拟机VM)运行着**Ubuntu操作系统**(这里以Ubuntu为例)。

      - 通过这个

        套娃行动👶

        ，我们可以进行类比：

        - 虚拟机(软件)是计算机系统的**仿真器**，通过软件模拟具有完整硬件系统功能的、运行在一个完全隔离环境中的、能提供物理计算机功能的**电脑**💻。

- 🆗我们已经理解了：

  - **虚拟机**就是在你自己的电脑上跑一个**仿真器**，这个**仿真器**模拟的同样是一个**电脑**。

#### [1.2 软件下载：](https://github.com/CCNU-IOT/CCNU-IOT-DOCS/blob/hardware-group/Linux/虚拟机安装.md#12-软件下载)

- 首先，需要**虚拟机**这个软件，并且能够适配你本地的**Windows操作系统**：

  - 这里我们使用`VMware Workstation Pro`这个软件，感兴趣的同学可以wiki一下：[VMware Workstation - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/VMware_Workstation)

  - 我们这里准备了安装方法(为了**白嫖**而生🐱)：

    - 我们下载`VMware Workstation 17 Pro`，(之前的文章还是使用的**16**😄)，安装包在**协会内部U盘**里面(飞书组织认证还没有成功，暂时不能使用云空间存储😢)。
    - [![image-20230930152409493](https://camo.githubusercontent.com/db06a0517ee3bbd86b7a98c9abc43a9df34d0e1ac1e269e89e5440fe084eb4b8/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135323430393439332e706e67)](https://camo.githubusercontent.com/db06a0517ee3bbd86b7a98c9abc43a9df34d0e1ac1e269e89e5440fe084eb4b8/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135323430393439332e706e67)
    - 鼠标**右键**，**管理员安装**🚗：
      - [![image-20230930153157209](https://camo.githubusercontent.com/893f7adb0079142290053393700ee6345bda3d97c0c3c1b491d407e948e7c29e/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333135373230392e706e67)](https://camo.githubusercontent.com/893f7adb0079142290053393700ee6345bda3d97c0c3c1b491d407e948e7c29e/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333135373230392e706e67)
      - 请更改你的**安装路径**⭕，如果你只有一个盘🆑，那么请**忽略**这句话。
      - [![image-20230930153320822](https://camo.githubusercontent.com/a26e3a95e581b839c2527d0be8d52cdc38c5bc836ddce41292b76f4c8c6bd57d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333332303832322e706e67)](https://camo.githubusercontent.com/a26e3a95e581b839c2527d0be8d52cdc38c5bc836ddce41292b76f4c8c6bd57d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333332303832322e706e67)
      - 不勾选任何选项，你的用户体验将**拉满**🎿。
      - [![image-20230930153407731](https://camo.githubusercontent.com/068b174b39147ce4134d7f51d3e1ba364eb1c8dcc53c3e654341660c470af776/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333430373733312e706e67)](https://camo.githubusercontent.com/068b174b39147ce4134d7f51d3e1ba364eb1c8dcc53c3e654341660c470af776/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333430373733312e706e67)
      - 一般来讲，**桌面**和**开始菜单**都有快捷方式比较方便，除非你是一个**洁癖**✌️。
    - **许可证**：
      - 我们的**白嫖**也不是不讲武德的，也是有**许可证**的🐶。
      - [![image-20230930153800052](https://camo.githubusercontent.com/c205bcd0b4d27cfc64406eb8b7b7a9b95199dd85a398bcded5721098d7a128e4/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333830303035322e706e67)](https://camo.githubusercontent.com/c205bcd0b4d27cfc64406eb8b7b7a9b95199dd85a398bcded5721098d7a128e4/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333830303035322e706e67)
      - 都到这了，我就不把许可证粘过来了，请自行填写🖊️。
    - **成功get**：
      - [![image-20230930153900543](https://camo.githubusercontent.com/27f3ec7fbc9ef651b2e0bb5f47f332a9ea2084a1b5f104e9e53578fdcd38d584/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333930303534332e706e67)](https://camo.githubusercontent.com/27f3ec7fbc9ef651b2e0bb5f47f332a9ea2084a1b5f104e9e53578fdcd38d584/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135333930303534332e706e67)

  - 开启电脑的**虚拟化**功能🤔：

    - 有了强大的虚拟机软件还不够，你的电脑也要支持虚拟机的运行✌️，通常情况下我们需要手动开启**虚拟化功能**。

    - 打开控制面板🚗：

      - 别问我怎么打开控制面板......
      - [![image-20230930154206522](https://camo.githubusercontent.com/6bbb33b31ea3e12c51bd37382b284b7d866ebcca727315478bfcc3e6f8bb563d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343230363532322e706e67)](https://camo.githubusercontent.com/6bbb33b31ea3e12c51bd37382b284b7d866ebcca727315478bfcc3e6f8bb563d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343230363532322e706e67)

    - 选择程序—启用或关闭Windows功能

      ：

      - [![image-20230930154253440](https://camo.githubusercontent.com/0ca337536366760ccb27e5d219ec6f452b1bb41bd1e10184d81b3ddcceb8668b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343235333434302e706e67)](https://camo.githubusercontent.com/0ca337536366760ccb27e5d219ec6f452b1bb41bd1e10184d81b3ddcceb8668b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343235333434302e706e67)

    - 💯勾选

      Hyper-V

      ：

      - 如果没有这个选项，也没有关系，貌似只有**专业版**有，这就是专业的力量⭕。
      - [![image-20230930154535214](https://camo.githubusercontent.com/74581175d021e80af4ab545702865821765ea47fc6f8b650b14bd845351b7c0d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343533353231342e706e67)](https://camo.githubusercontent.com/74581175d021e80af4ab545702865821765ea47fc6f8b650b14bd845351b7c0d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343533353231342e706e67)

    - 💯勾选

      虚拟机平台

      ：

      - 你不要跟我讲你没有这个选项，我不接受......
      - [![image-20230930154620946](https://camo.githubusercontent.com/c656f468d3e10ce0ddd52c5ed30512c4d6e7b2a94644d94e62099d82b04eaf9b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343632303934362e706e67)](https://camo.githubusercontent.com/c656f468d3e10ce0ddd52c5ed30512c4d6e7b2a94644d94e62099d82b04eaf9b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303135343632303934362e706e67)

    - 点击确定就🆗了，乖乖的重启电脑吧🤖。

- 虚拟机有了，还差点啥？**操作系统**呗🐧！

  - 不要给我扯什么别的，乖乖给我用**Ubuntu22.04**，除非你在搞**华为**的东西(**遥遥领先**的**Ubuntu18**)，我不是**黑子**⭕！

  - **.iso装载包**已经存到**协会内部U盘**里面了，请自行传输🐦。

  - 接下来开始安装🎿：

    - [![image-20230930161353164](https://camo.githubusercontent.com/a03fe954a03950e9923722a96ffa5e2f46a89fdbb7e88e1d91b7b2fffe6f4e3a/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313335333136342e706e67)](https://camo.githubusercontent.com/a03fe954a03950e9923722a96ffa5e2f46a89fdbb7e88e1d91b7b2fffe6f4e3a/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313335333136342e706e67)
    - [![image-20230930161544345](https://camo.githubusercontent.com/10f2bc24fdc6b3304497b256e3c7b89d24a39a087aa612295ef9b6e2a9fa5ce2/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313534343334352e706e67)](https://camo.githubusercontent.com/10f2bc24fdc6b3304497b256e3c7b89d24a39a087aa612295ef9b6e2a9fa5ce2/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313534343334352e706e67)
    - 找到**.iso装载包**的路径：
      - [![image-20230930161631801](https://camo.githubusercontent.com/f9aacc40d64db14f2b492c79412ea53094aa8a4d326cfecaa55e5ea948b3723c/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313633313830312e706e67)](https://camo.githubusercontent.com/f9aacc40d64db14f2b492c79412ea53094aa8a4d326cfecaa55e5ea948b3723c/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313633313830312e706e67)
      - [![image-20230930161707783](https://camo.githubusercontent.com/c117abc6f6a74cd4a40fc2a711437c3cb38db60443d69eeabe78d46239865611/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313730373738332e706e67)](https://camo.githubusercontent.com/c117abc6f6a74cd4a40fc2a711437c3cb38db60443d69eeabe78d46239865611/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313730373738332e706e67)
      - 密码短一点，不要**折磨自己**🤔！
      - 给你的**虚拟机**💻起一个有**标志性**的名称，可以像我一样在**D盘**创建一个专门的文件夹**存放系统**。
      - [![image-20230930161816344](https://camo.githubusercontent.com/2514108753ec8b2b436deb2d1eda4c9c42208133f6f3b949d9300f73b2247c63/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313831363334342e706e67)](https://camo.githubusercontent.com/2514108753ec8b2b436deb2d1eda4c9c42208133f6f3b949d9300f73b2247c63/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136313831363334342e706e67)
      - 磁盘大小**靓丽而行**😄(我有1T，所以比较豪爽)。
        - [![image-20230930162021837](https://camo.githubusercontent.com/b62c4ee85a8cec996c62f1bb74d5ffd24314aeb2426e52d36c5fb2d571e616b1/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323032313833372e706e67)](https://camo.githubusercontent.com/b62c4ee85a8cec996c62f1bb74d5ffd24314aeb2426e52d36c5fb2d571e616b1/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323032313833372e706e67)
      - **内存**选个**4G**就够了，如果不够后续再改：
        - [![image-20230930162104154](https://camo.githubusercontent.com/b8dc8e63e7499f57844f56eea97f01314486ebbbaab06d5c66578036311eaad6/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323130343135342e706e67)](https://camo.githubusercontent.com/b8dc8e63e7499f57844f56eea97f01314486ebbbaab06d5c66578036311eaad6/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323130343135342e706e67)
      - 配置完成，等待**Ubuntu22.04系统**的安装✌️。

  - **安装Ubuntu22.04**：

    - [![image-20230930162257700](https://camo.githubusercontent.com/62f58402e3322a5478f682f103de931370b4ee07971bd0cda22f24aedb89575a/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323235373730302e706e67)](https://camo.githubusercontent.com/62f58402e3322a5478f682f103de931370b4ee07971bd0cda22f24aedb89575a/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323235373730302e706e67)

    - 请选择**US**的键盘设置，不要告诉我**中国人要选中文键盘**😄，到时候报错有你**好果汁**吃！

    - [![image-20230930162431026](https://camo.githubusercontent.com/6f1bbe30cd7ca924a6adeb0cb8ccf4cfeca7040b610e9604262a0d08331f7490/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323433313032362e706e67)](https://camo.githubusercontent.com/6f1bbe30cd7ca924a6adeb0cb8ccf4cfeca7040b610e9604262a0d08331f7490/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323433313032362e706e67)

    - 选择**最小安装**，我是个**急性子**，不喜欢在安装系统的时候花太多时间🚗，按照上面的勾选直接`continue`即可。

    - [![image-20230930162638125](https://camo.githubusercontent.com/af81aa3aeeb2032a8679b1e94bbd8bca0f7342ffa0d49515e8136ada4676efe6/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323633383132352e706e67)](https://camo.githubusercontent.com/af81aa3aeeb2032a8679b1e94bbd8bca0f7342ffa0d49515e8136ada4676efe6/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323633383132352e706e67)

    - 按照这样选就行，如果是装**本地Ubuntu系统**，我推荐**手动分配**挂载点空间，放心，不会把你的磁盘都`erase`的❤️。

    - 时区选择

      上海

      (沪✌️)：

      - [![image-20230930162917372](https://camo.githubusercontent.com/44674125fbdebee907d15dee2d343033f4feee537cd33a4149fd51bb72046731/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323931373337322e706e67)](https://camo.githubusercontent.com/44674125fbdebee907d15dee2d343033f4feee537cd33a4149fd51bb72046731/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136323931373337322e706e67)

    - 密码

      和

      用户名

      短一点，不要折磨自己！

      - [![image-20230930163015506](https://camo.githubusercontent.com/cb24b87c1b9815d1c4e051fa3841394f6bbe9de8b934bcd3a854bb6d6af8fd5a/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333031353530362e706e67)](https://camo.githubusercontent.com/cb24b87c1b9815d1c4e051fa3841394f6bbe9de8b934bcd3a854bb6d6af8fd5a/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333031353530362e706e67)

    - 接下来，只管静静地等待~🤔

    - 最后的

      冲刺

      ：

      - [![image-20230930163847236](https://camo.githubusercontent.com/8e2bade9b3d4f6bbb825b30d8fcf48c29629a9044869bb9ea78ce965684ac741/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333834373233362e706e67)](https://camo.githubusercontent.com/8e2bade9b3d4f6bbb825b30d8fcf48c29629a9044869bb9ea78ce965684ac741/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333834373233362e706e67)
      - [![image-20230930163909319](https://camo.githubusercontent.com/f2ac677cc726e14284c1bc06b898cdcc49240be45dc9fd9e36c97fd9a6924b8c/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333930393331392e706e67)](https://camo.githubusercontent.com/f2ac677cc726e14284c1bc06b898cdcc49240be45dc9fd9e36c97fd9a6924b8c/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333930393331392e706e67)
      - [![image-20230930163939248](https://camo.githubusercontent.com/f2198be5fdf4749fc93f5b2e3b1b47e46e42d6bc3fa8d8bf5867120a77fe8c48/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333933393234382e706e67)](https://camo.githubusercontent.com/f2198be5fdf4749fc93f5b2e3b1b47e46e42d6bc3fa8d8bf5867120a77fe8c48/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333933393234382e706e67)
      - [![image-20230930163959888](https://camo.githubusercontent.com/afb1f338679c467533c999e7d5a2de65f62ecabb93da5928d6d461bfbb2d840b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333935393838382e706e67)](https://camo.githubusercontent.com/afb1f338679c467533c999e7d5a2de65f62ecabb93da5928d6d461bfbb2d840b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136333935393838382e706e67)
      - [![image-20230930164019924](https://camo.githubusercontent.com/2d2c56bb427b1b9f70e5360fd92e6296dd3ec2182d5a730ef9a001bf9cdd790d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136343031393932342e706e67)](https://camo.githubusercontent.com/2d2c56bb427b1b9f70e5360fd92e6296dd3ec2182d5a730ef9a001bf9cdd790d/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136343031393932342e706e67)
      - 所以，**Linux**也没那么可怕对吧！

  - 更换**软件源**：

    - 如果你不理解这是在干嘛，请咨询实验室的学长👨学姐👩，如果他们不能给你一个比较好的答复，请找我，因为这个东西一两句话说不清楚🤔，当然我也推荐你**Google**。

    - 在**虚拟机**中打开**火狐**🦊浏览器，输入以下地址：

      - ```
        https://mirror.tuna.tsinghua.edu.cn/help/ubuntu/
        ```

        

    - **复制**下面的内容：

      - [![image-20230930164318029](https://camo.githubusercontent.com/5311376df21929e9b1cc22f19118f1803011920b3ba217d110d6c0e103dae58b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136343331383032392e706e67)](https://camo.githubusercontent.com/5311376df21929e9b1cc22f19118f1803011920b3ba217d110d6c0e103dae58b/68747470733a2f2f6e69636b616c6a792d70696374757265732e6f73732d636e2d68616e677a686f752e616c6979756e63732e636f6d2f696d6167652d32303233303933303136343331383032392e706e67)

    - 打开**终端**：

      - ```
        ctrl + alt + t
        ```

        

      - 这是**快捷键**。

    - 执行如下**命令**：

      - ```
        sudo gedit /etc/apt/sources.list
        ```

        

      - 用刚刚复制的内容**替换掉**😄这里的内容，并且**保存**，**关掉编辑器**。

      - ```
        sudo apt update
        sudo apt upgrade
        ```

        

- 虚拟机的**最基本安装**已经搞定，接下来就靠你了，**船帆等待远航**🚢

## 2.clash安装及配置

### 2.1clash安装

### 2.1.1 下载地址：[Releases · Fndroid/clash_for_windows_pkg (github.com)](https://github.com/Fndroid/clash_for_windows_pkg/releases)

![image-20231007102212423](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071022513.png)

2.1.2下载好之后，放在虚拟机Ubuntu和Windows主机的共享文件夹里

![image-20231007102407612](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071024643.png)

打开文件其他位置![image-20231007110115302](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071101417.png)

打开计算机

![image-20231007110154712](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071101737.png)

打开mnt文件

![image-20231007110233636](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071102679.png)

打开hgfs

![image-20231007110305065](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071103098.png)

点击三个点，在终端打开

![image-20231007110444023](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071104073.png)



2.1.3通过tar -zxvf xxx.tar.gz 解压缩(因为我的终端已经关闭了，之前没有安装`tmux`终端多路复用器，无法查询关闭终端记录，这里我引用网上的截图)

```bash
tar -zxvf Clash for Windows-0.20.36-x64-linux.tar,gz
```

![image-20231007110528787](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071105863.png)

2.1.4

进入到解压缩目前，可以使用 ls 命令查看文件结构，里面会有一个 cfw 文件，这个就是启动程序，我们通过 ./cfw 启动 clash for windows

```bash
cd Clash for Windows-0.20.36-x64-linux
ls
./cfw
```

![image-20231007110642110](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071106306.png)

启动之后，会显示 clash for windows 的窗口，这样 clash for windows 的程序就启动了

![image-20231007111430038](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071114091.png)

### 2.1.5 导入节点

订阅链接后复制链接在 clash for windows 的 Profiles 托管刚才的链接 

![image-20231007111609977](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071116019.png)

托管完成后， 在 Proxies 里可以看到刚才托管的节点还有分流规则

![image-20231007111720899](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071117937.png)

### 2.1.6 设置代理

![image-20231007112007601](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071120722.png)



![image-20231007112042567](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071120645.png)

![image-20231007111950777](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071119822.png)

托管完成后，还不能翻墙，原因是要设置系统代理与 clash for windows 连接上才可以，7890 是 clash for windows 默认端口，127.0.0.1 是指向本机的 ip

这样所有的设置就完成了，打开浏览器，可以正常访问了。

## 3.git配置

### 3.1安装

一个全新的ubunt系统，需要安装Git（系统是不具有该工具的），方法如下：
在terminel中输入如下命令：

```csharp
sudo apt-get install git git-core git-gui git-doc git-svn git-cvs gitweb gitk git-email git-daemon-run git-el git-arch
```

**接下来需要检查SSH**

因为GitHub会用到SSH，因此需要在shell里检查是否可以连接到GitHub

```typescript
ssh -T git@github.com
```

如果看到：

> Warning: Permanently added ‘github.com,204.232.175.90’ (RSA) to the list of known hosts.
> Permission denied (publickey).

则说明可以连接。

## 3.1安装SSH keys(一定要在~/.ssh目录下操作)

在安装GitHub之前，需要先安装SSH keys

**第一步**：检查是否已井具有ssh keys，如果已经具有，则进行第二步，否则，进行第三步

```bash
cd ~/.ssh
ls
```

![image-20231007114024067](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071140104.png)

查看该目录下是否已经具有ssh keys，发现并没有id_rsa（私钥）和id_rsa.pub（公钥）这两个文件

**第二步**：备份并移除已经存在的ssh keys

```cobol
mkdir key_backup
cp id_rsa* key_backup
rm id_rsa* 
```

即将已经存在的id_rsa，id_rsa.pub文件备份到key_backup文件夹

**第三步**：执行如下命令（不具有ssh keys时）：

```csharp
ssh-keygen -t rsa -C "你自己的github对应的邮箱地址"
```

注1：“”是需要的！
注2：是在ssh目录下进行的！

得到结果如下：

![image-20231007114121994](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071141045.png)

发现，id_rsa（私钥）和id_rsa.pub（公钥）这两个文件被创建了
（通过ls查看～/.ssh下面的所有内容查看）

```bash
ls
```

**第四步**：将刚刚创建的ssh keys添加到github中
（1）利用gedit/cat命令，查看id_rsa.pub的内容

```bash
cat
```

（2）在GitHub中，依次点击Settings -> SSH Keys -> Add SSH Key，将id_rsa.pub文件中的字符串复制进去，注意字符串中没有换行和空格。

**第五步**：再次检查SSH连接情况（在～/.ssh目录下）：

输入如下命令：

```typescript
ssh -T git@github.com
```

如果看到如下所示，则表示添加成功：

> Hi 你的用户名! You’ve successfully authenticated, but GitHub does not provide shell access.

此时，发现github上已有了SSH keys

注1：之前在设置公钥时如果设置了密码，在该步骤会要求输入密码，那么，输入当时设置的密码即可。

注2：通过以上的设置之后，就能够通过SSH的方式，直接使用Git命令访问GitHub托管服务器了

注3：若在服务器添加完公钥后报错

```
sign_and_send_pubkey: signing failed: agent refused operation
```



这个时候我们只要执行下

```bash
eval "$(ssh-agent -s)"
ssh-add
```

就可以了

### 3.2  github使用

### 配置git

即利用自己的用户名和email地址配置git

```csharp
git config --global user.name "你的github用户名"
git config --global user.email "你的github邮箱地址"
```

记住空格不能少

### 如何推送本地内容到github上新建立的仓库

#### github上新建立仓库

具体内容不做介绍，假设，新建的仓库为dockerfiels

#### 在本地建立一个目录

该目录名称与github新建立的目录相同，假设本地目录为~/Document/dockerfiles

#### 本地仓库初始化

```typescript
cd ~/Document/dockerfiles
git init
```

#### 对本地仓库进行更改（在 ～/Document/dockerfiles 目录下执行)

例如，添加一个Readme文件

```bash
touch Readme
```

#### 对刚刚的更改进行提交

该步不可省略！

```sql
git add Readme
git commit -m 'add readme file'
```

#### push

首先，需要将本地仓库与github仓库关联
注：https://github.com/你的github用户名/你的github仓库.git 是github上仓库的网址

```cobol
git remote add origin https://github.com/你的github用户名/你的github仓库.git
```

然后，push，此时，可能需要输入github账号和密码，按要求输入即可

```perl
git push origin master
```

注：有时，在执行git push origin master时，报错：error:failed to push som refs to…….，那么，可以执行

```undefined
git pull origin master
```



### 如何推送本地内容到github上已有的仓库

#### 从github上将该仓库clone下来

```cobol
git clone https://github.com/你的github用户名/github仓库名.git
```

#### 对clone下来的仓库进行更改（在仓库目录下进行）

例如，添加一个新的文件

```bash
touch Readme_new
```

####  

#### 对刚刚的更改进行提交

该步不可省略！(其实是提交到git缓存空间)

```sql
git add Readme_new
git commit -m 'add new readme file'
```

#### push

首先，需要将本地仓库与github仓库关联
注：https://github.com/你的github用户名/你的github仓库.git 是github上仓库的网址

```cobol
git remote add origin https://github.com/你的github用户名/你的github仓库.git
```

有时，会出现fatal: remote origin already exists.，那么，需要输入git remote rm origin 解决该问题

然后，push，此时，可能需要输入github账号和密码，按要求输入即可

```perl
git push origin master
```

注：有时，在执行git push origin master时，报错：error:failed to push som refs to…….，那么，可以执行

```undefined
git pull origin master
```

至此，github上已有的仓库的便有了更新



## 小结命令

- 克隆github上已有的仓库

```cobol
git clone https://github.com/你的github用户名/github仓库名.git
```



- 或者是在github上新建仓库并且在本地新建同名的仓库

```typescript
cd ~/Document/dockerfiles
git init
```



- 对本地仓库内容进行更改（如果是多次对本地的某个仓库进行这样的操作，直接从此步开始即可，不要前面的操作了，因为本地仓库已有具有了github仓库的.git文件了）
- 对更改内容进行提交

```sql
git add 更改文件名或者是文件夹名或者是点"."
git commit -m "commit内容标注"
```

- 本地仓库与github仓库关联

```cobol
git remote add origin https://github.com/你的github用户名/你的github仓库.git 
```



- push

```perl
git push origin master
```

注：另外可能用到的命令

```bash
git remote rm origin
git pull origin master
```

------

## 查看当前git缓存空间状态

```lua
git status
```