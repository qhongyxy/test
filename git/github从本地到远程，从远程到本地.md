# 一.安装

## 1.git及github Destop一键安装包

**百度云盘**

链接：https://pan.baidu.com/s/1gPXpt9-MhmPFG2PQXcyEHw 提取码：la4i

- 这个github Destop是可视化的git

加快百度网盘下载速度达10Mb/s的官方免费方法：

[百度网盘10M/s开启技巧_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Pu4y127kL/?spm_id_from=333.999.0.0&vd_source=3b09dd0fe60220d7ade99b728178eb29)

## 2.github Destop汉化包

[robotze/GithubDesktopZhTool: Github Desktop 汉化工具 支持 Windows Mac Linux](https://github.com/robotze/GithubDesktopZhTool)

教程：

1.点进链接后，

![](C:\Users\wangq\AppData\Roaming\Typora\typora-user-images\image-20230930175244015.png

![image-20230930175351558](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070029021.png)

点击这个

2.跳转后，再点下载符号![image-20230930175432200](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070029617.png)

3.点击下载好的路径，打开这个文件夹

![image-20230930175612875](C:\Users\wangq\AppData\Roaming\Typora\typora-user-images\image-20230930175612875.png)

4.点击下方的exe程序

![image-20230930175641761](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070030648.png)

5点击汉化，提示汉化成功后，重启github Destop，就可以发现现在是中文界面了

# 二.git环境搭建

### 一.配置环境变量

1.打开电脑开始，点击控制面板

2.找到系统

![image-20231007003414261](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070034319.png)

![image-20230930180304399](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070030393.png)

3.然后点击高级系统设置

![image-20230930182747128](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070034842.png)

4.然后进入环境变量，找到系统的path，点击编辑

![image-20230930182838341](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070030283.png)

5.点击新建

![image-20230930180554005](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310070034812.png)

6将你安装git时选择的文件夹的路径复制过来

然后点击确定，一共是三次，都要点。

### 二.检测是否配置成功

1.找到你安装路径下的git for windows文件夹

![image-20230930181101328](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071546948.png)

2.然后ctrl+L再输入cmd,enter键之后就从cmd进入当前文件夹下

![image-20230930181311437](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071546076.png)

3.输入git --version

显示出版本号，则表示成功

# 三.git初始配置

### 1.Git的初始配置

**1、开启Git终端**
安装成功后在桌面的开始菜单会多了3个git XXX（分别是：git bash、git gui、git cmd），点击**git bash**，即可启动git终端。
**2、绑定Git的用户名及邮箱**
进入终端后，先输入下面的代码：

```lua
git config --global user.name  (这里是官网注册的用户名)
git config --global user.email (这里是官网注册的邮箱)
```

如下图：
![image-20230930181637281](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071546756.png)

![image-20230930181731734](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071546372.png)

**3、创建Git的本地仓库与远程仓库**
我们将自己本地的代码或者项目上传至GitHub服务器中实质上时我们在自己的本地建立一个装项目的“仓库”，然后通过Internet连接上传到位于远程服务器里自己的“仓库”中，具体这个远程的“仓库”里的代码是否要共享就看自己的设置了。这里我们介绍如何建立这两个“仓库”。
**3.1、创建Git的本地仓库**
例如，我们想要把本地磁盘E盘里的whq_demo文件夹作为本地仓库：
方法一：直接在E盘里创建名为whq_demo的文件夹即可，然后将自己想要上传的项目复制到这个文件夹里
方法二：在git bash终端中先进入E盘的目录，然后利用mkdir命令新建名为whq_demo的文件夹，然后将自己想要上传的项目复制到这个文件夹里：
![image-20230930181831035](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071546651.png)
大家可以看到我在E盘新建了两个本地仓库。

创建好后，你可以在E盘中看到新创建的文件

**3.2、创建Git的远程仓库**
进入官网，用我们自己的账户登录进去后，点击右上角的“+”号，然后选择“New repository”：
![image-20230930182021837](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071548611.png)
接着我们可以设置这个仓库的具体属性：我这个仓库已经创建了。所以提醒我重名了
![image-20231007155004370](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071550435.png)设置完毕后点击Add即可生成远程仓库。

### 2.本地Git与远程GitHub连接的建立

**这一步操作至关重要，只有将Git本地与远程的GitHub建立了连接以后我们本地的项目才能上传至远程服务器**
**1、Git终端的配置，生成公钥文件，用来连接github**
在git终端输入如下命令，**然后连续敲3个回车即可**：
`ssh-keygen -t rsa -C (这里是你的邮箱地址)`这个C是大写
效果如下：
![image-20230930182332768](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071550796.png)
**2、本地的配置**
2.1 命令执行成功后，**在本地电脑的C:\Users\下的名为.ssh的目录下找到名为id_rsa.pub的文件，打开这个文件后将里面的内容先复制下来；**这个pub文件，你可用WPS打开

![image-20230930182447587](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071550067.png)2.2 这里还需要进行的一步操作是：为了防止git连接失败，可在.ssh文件夹下新建一个**无后缀的名称为config的文件**，在里面加入下面代码：

```javascript
Host github.com
User git 
Hostname ssh.github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa
Port 443
```

**3、远程的配置**
**进入到GitHub的官网，点击右上角图标下的settings:**
![image-20230930183003409](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071550824.png)
**然后，在出现的左边的settings栏目中选择SSH and GPG Keys：**
![image-20230930183035628](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071550837.png)
**然后在出来的左边的框框中选择 New SSH：**

![image-20230930183157615](C:\Users\wangq\AppData\Roaming\Typora\typora-user-images\image-20230930183157615.png)

**弹出下图：**
其中Title可以随意写个名字，**Key里面的内容需要将2.1步中复制的id_rsa.pub文件中的内容拷贝进去，注意不是config文件的代码！**最后点击Add即可。

![image-20230930183233351](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071550581.png)

、**4、验证连接是否成功建立**
在git终端上输入如下命令：

```css
ssh -T git@github.com
```

如果出现下图所示的内容说明连接成功

![image-20230930183336479](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071551261.png)


如果出现错误可以尝试通过执行 `ssh -T -p 22 git@github.com` 命令来解决，其中-p 22表示将服务器端口改为22。

### 3.将本地项目上传到GitHub远程服务器

**其实，这个过程的实质就是在我们之前创建好的本地仓库与远程仓库之间利用建立好的连接进行项目的上传。**
**1、包含需要上传项目的本地仓库的配置**
1.1 在前面的介绍中，我们已经将自己的项目赋值到了本地仓库——名为whw_demo的文件夹中。现在我们需要在git终端进入这个仓库，然后在里面输入命令：
`git init`
效果如下（同时会在本地生成一个隐藏的init文件）：
![image-20230930183420588](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071551085.png)



![image-20230930183453176](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071551788.png)

1.2 我们上传的项目的名称为WHW_FTP(已将该文件拷贝到whw_demo文件夹下)，然后将这个项目提交到仓库中：
`git add WHW_FTP`
效果如下：
![image-20230930183525094](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071551364.png)



1.3 接着运行下面代码（注意-m后面是注释内容）:
`git commit -m whw_ftp`
效果如下（由于图太长只截取了部分）：



![image-20230930183550035](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071551109.png)

这里需要说明的是：
（1）git add . #就可以把所有内容添加到索引库中，注意后面有个点，而且add和点之间有空格
（2）git commit -m “注释内容” #提交索引库中的内容，-m是参数，表示注释内容，主要用来记录此次操作
1.4 然后运行下面代码：
`git remote add origin git@github.com:UserName/RepertoryName.git`
其中git@github.com:UserName/RepertoryName.git是我们github中仓库的ssh地址，UserName处是用户名，RepertoryName处github远程仓库名（如之前创建的test仓库）。
然后，再输入下面代码：
`git push -u origin master`
效果如下：
![image-20230930183739875](https://cdn.jsdelivr.net/gh/qhongyxy/Internetimg/202310071551093.png)
最后，我们在GitHub官网中自己的test远程仓库中可以看到该项目已经上传成功了！





最后需要说明的一点是，如果本地仓库为空是不能提交的，如果运行`git push -u origin master`出现error错误，一般情况下都是仅进行了init操作，没有进行add与commit操作