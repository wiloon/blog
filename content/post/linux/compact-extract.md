---
title: compact/extract 压缩/解压
author: "-"
date: 2022-09-16 12:17:27
url: "compact-extract"
categories:
  - Command
tags:
  - Linux
  - Command

---
## compact/extract 压缩/解压

## .tar.gz 和 .tgz

.tgz 和 .tar.gz 是同一个东西, .tgz 可以认为是 .tar.gz 是简写, 在远古时代比如 DOS 系统, 文件扩展名只能是三个字符, 所以有了 .tgz,
后来限制解除之后就能支持 .tar.gz 这种后缀了, 后者能更清晰地表达打包格式和压缩方式.

[https://stackoverflow.com/questions/11534918/are-tar-gz-and-tgz-the-same-thing](https://stackoverflow.com/questions/11534918/are-tar-gz-and-tgz-the-same-thing)

这种格式是我使用得最多的压缩格式。它在压缩时不会占用太多 CPU 的，而且可以得到一个非常理想的压缩率  
默认 tar 打包和系统默认的压缩工具是单线程的，`pigz` 是 gzip 的多线程实现, 默认用当前逻辑 cpu 个数来并发压缩，无法检测个数的话，则并发8个线程

### 压缩

```bash
tar -czvf all.tar.gz *.jpg

# 排除掉文件
tar -czvf tomcat.tar.gz --exclude=tomcat/logs tomcat

# 设置压缩级别
GZIP=-9 tar cvzf file.tar.gz /path/to/directory
```

### 压缩到指定目录

```bash
tar -zcvf /data/tmp/foo.tar.gz /data/server/source
# 解压到指定目录
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.6.1.tgz
```

### tar.gz 解压

```bash
tar -xf foo.tar.gz
# 解压 tar.gz 文件时, 不使用 z 参数, 貌似 tar 会检测文件类型 自动 用 gzip 解压...
tar xvf all.tar.gz
tar zxvf all.tar.gz
tar -zxvf all.tar.gz
```

### 解压到指定目录

```bash
tar zxvf /path/to/foo.tar.gz -C /path/to/target/dir/
tar -zxvf /path/to/foo.tar.gz -C /path/to/target/dir/
```

```bash
sudo pacman -S pigz
# 压缩
tar --use-compress-program=pigz -cvpf package.tgz ./package
# 解压
tar --use-compress-program=pigz -xvpf package.tgz -C ./package

#tar –use-compress-program=pigz表示指定pigz来进行打包
#c表示create创建 x表示extract解压 v表示verbose详细 f表示指定压缩文件 C表示指定目录
#-cvpf package.tgz ./ 表示将./package目录打包为package.tgz
#-xvpf package.tgz -C ./表示将package.tgz解压到./package目录下
```

```bash-c, --create #建立新的存档
\-v, --verbose #详细显示处理的文件
\-f, --file [HOSTNAME:]F #指定存档或设备 (缺省为 /dev/rmt0)
\-z, --gzip, --ungzip #用 gzip 对存档压缩或解压
\-x, --extract, --get #从存档展开文件
```

## 解压多个文件

```bash
ls *.gz|xargs -t -n1 gunzip
gunzip *.gz
```

## .rar

```bash
# 解压
unrar x foo.rar
# 压缩
rar e FileName.rar
# 解压
rar a FileName.rar
```

### 解压并指定输出目录

```bash
gunzip -c /data/tmp/foo.tar.gz | tar xf - -C /data/server/bar
```

## .7z

```bash
yum install p7zip
pacman -S p7zip
sudo apt install p7zip-full p7zip-rar

# 压缩
7z a -t7z -r manager.7z /home/manager/*
# a 代表添加文件/文件夹到压缩包
# -t 是指定压缩类型 一般我们定为7z
# -r 表示递归所有的子文件夹，manager.7z 是压缩好后的压缩包名，/home/manager/* 是要压缩的目录，＊是表示该目录下所有的文件。

7z x filename.7z
```

## .zip

```bash
pacman -S zip unzip
```

### zip 压缩

```bash
zip all.zip *.jpg

# 指定压缩文件目录
zip ~/all.zip *.jpg

# 压缩的是个文件夹, -r 表示调用递归压缩
zip -r temp.zip temp
# 密码
zip -P password0 foo.zip foo.txt       
# 指定压缩某几个文件
zip foo.zip foo.txt bar.txt
```

### zip 分卷压缩

```bash
# 分卷压缩的话，需要先将文件打包成一个zip包，然后执行
zip -s SIZE origin.zip --out new.zip

# SIZE为分卷的大小4m,4g,4t等
# 解压的时候需要先将它合并才能正常解压
zip spiltfile.zip -s=0 --out single.zip
```

### zip 解压

```bash
unzip all.zip
unzip -o -d /home/sunny myfile.zip

# 解压 多个文件
ls *.zip | xargs -n1 unzip -o

# -o: 不必先询问用户，unzip执行后覆盖原有的文件；
# -P<密码>: 使用zip的密码选项；
# -d 指定解压的目标目录

# 解压最近4天的zip文件

find . -maxdepth 1 -mtime -4 -type f  -name "*.zip"|xargs -t -n1 unzip
```

### zip 解压并指定目录

```bash
unzip /path/to/source.zip -d /path/to/target/path
```

## Zstandard, zstd, .zst

### 解压

```bash
zstd -d foo.zst

```

zstd 不能压缩目录, -r 参数会把目录里的文件压缩成单独的文件

### .tar.zst

tar 从 1.30.90 之后开始支持 zstd
有些发行版默认没有安装 zstd 需要安装一下, 比如 `dnf install zstd`

```bash
# 压缩
tar -I zstd -cvf foo.tar.zst foo

# 解压
tar -I zstd -xvf foo.tar.zst
```

### .zst

```bash
# -z 压缩, 不加参数，默认为压缩
zstd foo.txt
zstd -z foo.txt

# -d 解压
zstd -d foo.txt.zst
unzstd foo.txt.zst

# 指定压缩级别 1-19 默认3
zstd -6 foo.txt

# 线程数, 线程数为 0 时 zstd 会自动检测 cpu 核心数
zstd -T0 foo.txt
# --rm 压缩后删除原文件
```

## .tar

tar 命令可以把多个文件打包成一个文件, 还可以向 tar 包里添加文件或提取某一个文件.  tar 最初被用来在磁带上创建归档文件.  
Tar 是在 Linux 中使用得非常广泛的文档打包格式。它的好处就是它只消耗非常少的 CPU 以及时间去打包文件，tar 仅仅只是一个打包工具，没有压缩的功能。  

```Bash
dnf install tar gzip
```

```bash
# 打包: -c 是表示产生新的包，-f 指定包的文件名。
tar cvf FileName.tar DirName

# 解包:
tar xvf FileName.tar

# 将目录 logs 打包压缩并分割成多个 1M 的文件
tar cjf - logs/ |split -b 1m - logs.tar.bz2.

# 合并文件
cat logs.tar.bz2.a* | tar xj

# 指定操作目录
tar -zcf foo.tar.gz -C ${war_path} .
# 解压的时候用 -C, 比如当前目录是 /root, 执行以下命令, 会把 文件 /path/to/foo.tar.gz 解压到 /tmp
tar zxvf /path/to/foo.tar.gz -C /tmp

# tar xxx.tar --strip 1，--strip 1 的意思是表明把解压文件的内容里的所有最上层目录去掉。
tar xvf /backup/bitwarden-data.tar -C /tmp --strip 1
```

### BSD tar VS GNU tar

Mac 打包的 tar.gz 在 archlinux 解压时报错
>tar: Ignoring unknown extended header keyword 'LIBARCHIVE.xattr.com.apple.provenance'

Mac is built based on BSD by default. So, we can use a bunch of command on Linux without installing. But, if you use Mac with CentOS in parallel, you will get trouble which caused by the difference between Mac and CentOS environments.

```bash
# 在 Mac OS 上安装 GNU tar
brew install gnu-tar
# 查看 GNU tar  版本
gtar --version
# 用 GNU tar 打包+压缩
gtar czvf example.tar.gz example
```

[https://superuser.com/questions/318809/linux-os-x-tar-incompatibility-tarballs-created-on-os-x-give-errors-when-unt](https://superuser.com/questions/318809/linux-os-x-tar-incompatibility-tarballs-created-on-os-x-give-errors-when-unt)

[https://medium.com/@fullsour/installing-gnu-tar-on-mac-827a494b1c1](https://medium.com/@fullsour/installing-gnu-tar-on-mac-827a494b1c1)

### 向已有的 tar 包里增加文件

这条命令是将所有.gif的文件增加到all.tar的包里面去。-r是表示增加文件的意思。

```bash
tar -rf all.tar *.gif
```

### tar 参数

```bash
-c, --create : 创建新的压缩文件
-z : 用 gzip 压缩或解压
-x : 从压缩的文件中提取文件
-v : 打包过程中打印文件名
-f, --file=ARCHIVE : 指定文件或设备, 如果不加这个参数 tar 默认会去找环境变量里配置的 TAPE, 注意，在 f 之后要立即接文件名, 不要再加其它参数, 例如使用『tar -zcvfP tfile sfile』就是错误的写法，要写成 『tar -zcvPf tfile sfile』才对
-t : 查看 tarfile 里面的文件, 特别注意，在参数的下达中， c/x/t 仅能存在一个！不可同时存在因为不可能同时压缩与解压缩。 
-j : 是否同时具有 bzip2 的属性？亦即是否需要用 bzip2 压缩？
-p : 使用原文件的原来属性 (属性不会依据使用者而变)  
-P : 可以使用绝对路径来压缩！ 
-N : 比后面接的日期(yyyy/mm/dd)还要新的才会被打包进新建的文件中！ 
--exclude FILE: 在压缩的过程中，不要将 FILE 打包！  
-C : 在执行后续的指令前切换目录, 此参数是顺序敏感的.
-A 新增压缩文件到已存在的压缩
-B 设置区块大小
-d 记录文件的差别
-r 添加文件到已经创建好的 tar 包里追加文件
-u 更新文件。就是说，用新增的文件取代原备份文件，如果在备份文件中找不到要更新的文件，则把它追加到备份文件的最后。
-Z 支持compress解压文件
-l 文件系统边界设置
-k 保留原有文件不覆盖
-m 保留文件不被覆盖
-W 确认压缩文件的正确性

可选参数如下: 
-b 设置区块数目
-C 切换到指定目录, 比如解压到某一个目录
-f 指定压缩文件
-help 显示帮助信息
-version 显示版本信息
```

## .gz

```bash
# 压缩
# 直接压缩文件, 压缩成功之后默认会把原文件删掉, 变成 foo.txt.gz
gzip foo.txt

# 压缩 tar 文件到 .tar.gz
gzip foo.tar

# 解压1
gunzip FileName.gz
# 解压2
gzip -d FileName.gz
```

### .tar.bz2

这种压缩格式是我们提到的所有方式中压缩率最好的。当然，这也就意味着，它比前面的方式要占用更多的CPU与时间。

bzip2 -d foo.tar.bz2

## .xz

解压: xz -d foo.xz

```bash
#.tar.xz
$xz -d ***.tar.xz
$tar -xvf  ***.tar

#按时间打包
tar -czf log.tar.gz *.zip -N 2016/04/20
tar -xf all.tar

unrar x /media/data/homes-backup.rar homes-backup/
```

---

t 列出档案文件的内容，查看已经备份了哪些文件。

k 保存已经存在的文件。例如我们把某个文件还原，在还原的过程中，遇到相同的文件，不会进行覆盖。

m 在还原文件时，把所有文件的修改时间设定为现在。

M 创建多卷的档案文件，以便在几个磁盘中存放。

w 每一步都要求确认。

### Linux下的压缩文件剖析

对于刚刚接触Linux的人来说，一定会给Linux下一大堆各式各样的文件名 给搞晕。别个不说，单单就压缩文件为例，我们知道在Windows下最常见的压缩文件就只有两种，一是,zip，另一个是.rar。可是Linux就不同 了，它有.gz、.tar.gz、tgz、bz2、.Z、.tar等众多的压缩文件名，此外windows下的.zip和.rar也可以在Linux下使 用，不过在Linux使用.zip和.rar的人就太少了。本文就来对这些常见的压缩文件进行一番小结，希望你下次遇到这些文件时不至于被搞晕:)

在具体总结各类压缩文件之前，首先要 弄清两个概念: 打包和压缩。打包是指将一大堆文件或目录什么的变成一个总的文件，压缩则是将一个大的文件通过一些压缩算法变成一个小文件。为什么要区分这 两个概念呢？其实这源于Linux中的很多压缩程序只能针对一个文件进行压缩，这样当你想要压缩一大堆文件时，你就得先借助另外的工具将这一大堆文件先打 成一个包，然后再就原来的压缩程序进行压缩。

Linux下最常用的打包程序就是tar了，使用tar程序打出来的包我们常称为tar包，tar包文件的命令通常都是以.tar结尾的。生成tar包后，就可以用其它的程序来进行压缩了，所以首先就来讲讲tar命令的基本用法:

tar命令的选项有很多(用man tar可以查看到)，但常用的就那么几个选项，下面来举例说明一下:

tar -uf all.tar logo.gif

这条命令是更新原来tar包all.tar中logo.gif文件，-u是表示更新文件的意思。

tar -tf all.tar

这条命令是列出all.tar包中所有文件，-t是列出文件的意思

tar -xf all.tar

这条命令是解出all.tar包中所有文件，-x是解包的意思

以上就是tar的最基本的用法。为了方便用户在打包解包的同时可以压缩或解压文件，tar提供了一种特殊的功能。这就是tar可以在打包或解包的同时调用其它的压缩程序，比如调用gzip、bzip2等。

### tar调用bzip2

bzip2是一个压缩能力更强的压缩程序，.bz2结尾的文件就是bzip2压缩的结果。与bzip2相对的解压程序是bunzip2。tar中使用-j这个参数来调用bzip2。下面来举例说明一下:

tar -cjf all.tar.bz2 *.jpg

这条命令是将所有.jpg的文件打成一个tar包，并且调用bzip2压缩，生成一个bzip2压缩过的包，包名为all.tar.bz2

tar -xjf all.tar.bz2

这条命令是将上面产生的包解开。

3)tar调用compress

compress也是一个压缩程序，但是好象使用compress的人不如gzip和bzip2的人多。.Z结尾的文件就是bzip2压缩的结果。与compress相对的解压程序是uncompress。tar中使用-Z这个参数来调用gzip。下面来举例说明一下:

tar -cZf all.tar.Z *.jpg

这条命令是将所有.jpg的文件打成一个tar包，并且调用compress压缩，生成一个uncompress压缩过的包，包名为all.tar.Z

tar -xZf all.tar.Z

这条命令是将上面产生的包解开

有了上面的知识，你应该可以解开多种压缩文件了，下面对于tar系列的压缩文件作一个小结:

1)对于.tar结尾的文件

tar -xf all.tar

2)对于.gz结尾的文件

gzip -d all.gz

gunzip all.gz

4)对于.bz2结尾的文件

bzip2 -d all.bz2

bunzip2 all.bz2

5)对于tar.bz2结尾的文件

tar -xjf all.tar.bz2

6)对于.Z结尾的文件

uncompress all.Z

7)对于.tar.Z结尾的文件

tar -xZf all.tar.z

另外对于Window下的常见压缩文件.zip和.rar，Linux也有相应的方法来解压它们:

2)对于.rar

要在linux下处理.rar文件，需要安装RAR for Linux，可以从网上下载，但要记住，RAR for Linux

不是免费的；然后安装:

tar -xzpvf rarlinux-3.2.0.tar.gz

cd rar

make

这样就安装好了，安装后就有了rar和unrar这两个程序，rar是压缩程序，unrar是解压程序。它们的参数选项很多，这里只做简单介绍，依旧举例说明一下其用法:

rar a all *.jpg

这条命令是将所有.jpg的文件压缩成一个rar包，名为all.rar，该程序会将.rar 扩展名将自动附加到包名后。

unrar e all.rar

这条命令是将all.rar中的所有文件解压出来

到此为至，我们已经介绍过linux下的tar、gzip、gunzip、bzip2、bunzip2、compress、uncompress、 zip、unzip、rar、unrar等程式，你应该已经能够使用它们对.tar、.gz、.tar.gz、.tgz、.bz2、.tar.bz2、. Z、.tar.Z、.zip、.rar这10种压缩文件进行解压了，以后应该不需要为下载了一个软件而不知道如何在Linux下解开而烦恼了。而且以上方 法对于Unix也基本有效。

本文介绍了linux下的压缩程式tar、gzip、gunzip、bzip2、bunzip2、 compress、uncompress、zip、unzip、rar、unrar等程式，以及如何使用它们对.tar、.gz、.tar.gz、. tgz、.bz2、.tar.bz2、.Z、.tar.Z、.zip、.rar这10种压缩文件进行操作。

.bz2

解压1: bzip2 -d FileName.bz2

解压2: bunzip2 FileName.bz2

压缩:  bzip2 -z FileName

.tar.bz2

解压: tar jxvf FileName.tar.bz2

压缩: tar jcvf FileName.tar.bz2 DirName

———————————————

.bz

解压1: bzip2 -d FileName.bz

解压2: bunzip2 FileName.bz

压缩: 未知

.tar.bz

解压: tar jxvf FileName.tar.bz

压缩: 未知

———————————————

.Z

解压: uncompress FileName.Z

压缩: compress FileName

.tar.Z

解压: tar Zxvf FileName.tar.Z

压缩: tar Zcvf FileName.tar.Z DirName

.lha

解压: lha -e FileName.lha

压缩: lha -a FileName.lha FileName

lha请到: [http://www.infor.kanazawa-it.ac.jp/…/lhaunix/](http://www.infor.kanazawa-it.ac.jp/…/lhaunix/)下载！

解压后请将lha拷贝到/usr/bin目录 (其他由$PATH环境变量指定的目录也可以) :

cp lha /usr/bin/

### .rpm

解包: rpm2cpio FileName.rpm | cpio -div

.lzx .lzs .arc .sda .sfx .lnx .zoo .cab .kar .cpt .pit .sit .sea

解压: sEx x FileName.*

压缩: sEx a FileName.* FileName

sEx只是调用相关程序，本身并无压缩、解压功能，请注意！

sEx请到:  [http://sourceforge.net/projects/sex](http://sourceforge.net/projects/sex)下载！

解压后请将sEx拷贝到/usr/bin目录 (其他由$PATH环境变量指定的目录也可以) :

[root@www2 tmp]# cp sEx /usr/bin/

## 压缩算法, deflate、gzip、bzip2、lzo、snappy

[http://www.infoq.com/cn/news/2017/07/eBay-shopping-i-o?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global](http://www.infoq.com/cn/news/2017/07/eBay-shopping-i-o?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)

常用的压缩算法主要有: deflate、gzip、bzip2、lzo、snappy等。差别如下所示:

deflate、gzip都是基于LZ77算法与哈夫曼编码的无损数据压缩算法，gzip只是在deflate格式上增加了文件头和文件尾；

bzip2是Julian
  
Seward开发并按照自由软件/开源软件协议发布的数据压缩算法，Apache的Commons-compress库中进行了实现；

LZO致力于解压速度，并且该算法也是无损算法；

LZ4是一种无损数据压缩算法，着重于压缩和解压缩速度；

Snappy是Google基于LZ77的思路用C++语言编写的快速数据压缩与解压程序库，2011年开源。它的目标并非最大程度地压缩，而是针对最快速度和合理的压缩率。

---

[https://blog.csdn.net/wuhenyan/article/details/53117642](https://blog.csdn.net/wuhenyan/article/details/53117642)

[https://www.howtoing.com/zstd-fast-data-compression-algorithm-used-by-facebook](https://www.howtoing.com/zstd-fast-data-compression-algorithm-used-by-facebook)

[https://blog.csdn.net/lj402159806/article/details/76618174](https://blog.csdn.net/lj402159806/article/details/76618174)

[http://blog.csdn.net/silvervi/article/details/6325698](http://blog.csdn.net/silvervi/article/details/6325698)

[http://blog.csdn.net/xiaotuni/article/details/2099609](http://blog.csdn.net/xiaotuni/article/details/2099609)

[http://xxw8393.blog.163.com/blog/static/37256834201172910058899/](http://xxw8393.blog.163.com/blog/static/37256834201172910058899/)
