---
title: 时区, 日期格式, UTC、CST、GMT, RFC3339
author: "-"
date: 2016-03-09T01:58:55+00:00
url: timezone
categories:
  - Inbox
tags:
  - reprint
---
## 时区, 日期格式, UTC、CST、GMT, RFC3339

### 全球24个时区的划分

相较于两地时间表,可以显示世界各时区时间和地名的世界时区表 (World Time) ,就显得精密与复杂多了,通常世界时区表的表盘上会标示着全球24个时区的城市名称,但究竟这24个时区是如何产生的？过去世界各地原本各自订定当地时间,但随着交通和电讯的发达,各地交流日益频繁,不同的地方时间,造成许多困扰,于是在西元1884年的国际会议上制定了全球性的标准时,明定以英国伦敦格林威治这个地方为零度经线的起点 (亦称为本初子午线) ,并以地球由西向东每24小时自转一周360°,订定每隔经度15°,时差1小时。而每15°的经线则称为该时区的中央经线,将全球划分为24个时区,其中包含23个整时区及180°经线左右两侧的2个半时区。就全球的时间来看,东经的时间比西经要早,也就是如果格林威治时间是中午12时,则中央经线15°E的时区为下午1时,中央经线30°E时区的时间为下午2时；反之,中央经线15°W的时区时间为上午11时,中央经线30°W时区的时间为上午10时。以台湾为例,台湾位于东经121°,换算后与格林威治就有8小时的时差。如果两人同时从格林威治的0°各往东、西方前进,当他们在经线180°时,就会相差24小时,所以经线180°被定为国际换日线,由西向东通过此线时日期要减去一日,反之,若由东向西则要增加一日。

### 世界协调时间 UTC

多数的两地时间表都以 GMT 来表示, 但也有些两地时间表上看不到 GMT 字样, 出现的反而是 UTC 这3个英文字母, 究竟何谓UTC？事实上,UTC 指的是 Coordinated Universal Time－ 世界协调时间 (又称世界标准时间、世界统一时间), 是经过平均太阳时(以格林威治时间GMT为准)、地轴运动修正后的新时标以及以「秒」为单位的国际原子时所综合精算而成的时间,计算过程相当严谨精密,因此若以「世界标准时间」的角度来说, **UTC 比 GMT 来得更加精准**。其误差值必须保持在 0.9 秒以内, 若大于 0.9 秒则由位于巴黎的国际地球自转事务中央局发布闰秒, 使 UTC 与地球自转周期一致。所以基本上 UTC 的本质强调的是比GMT 更为精确的世界时间标准, 不过对于现行表款来说, GMT 与 UTC 的功能与精确度是没有差别的。
  
UTC 是协调世界时(Universal Time Coordinated)英文缩写, 是由国际无线电咨询委员会规定和推荐, 并由国际时间局(BIH)负责保持的以秒为基础的时间标度。UTC相当于本初子午线(即经度0度)上的平均太阳时,过去曾用格林威治平均时(GMT)来表示.
  
北京时间比UTC时间早8小时, 以1999年1月1日0000UTC为例, UTC时间是零点, 北京时间为1999年1月1日早上8点整。

### GMT(Greenwich Mean Time) 格林威治标准时间 GMT

十七世纪, 格林威治皇家天文台为了海上霸权的扩张计画而进行天体观测。1675 年旧皇家观测所 (Old Royal Observatory) 正式成立, 到了 1884 年决定以通过格林威治的子午线作为划分地球东西两半球的经度零度。观测所门口墙上有一个标志24小时的时钟,显示当下的时间,对全球而言,这里所设定的时间是世界时间参考点, 全球都以格林威治的时间作为标准来设定时间, 这就是我们耳熟能详的「格林威治标准时间」(Greenwich Mean Time,简称G.M.T.) 的由来, 标示在手表上, 则代表此表具有两地时间功能, 也就是同时可以显示原居地和另一个国度的时间。
  
由于地球轨道并非圆形,其运行速度又随着地球与太阳的距离改变而出现变化,因此视太阳时欠缺均匀性。视太阳日的长度同时亦受到地球自转轴相对轨道面的倾斜度所影响。为着要纠正上述的不均匀性,天文学家计算地球非圆形轨迹与极轴倾斜对视太阳时的效应。平太阳时就是指经修订后的视太阳时。在格林尼治子午线上的平太阳时称为世界时(UT0),又叫格林尼治平时(GMT)。 为了确保协调世界时与世界时(UT1)相差不会超过0.9秒,有需要时便会在协调世界时内加上正或负闰秒。因此协调世界时与国际原子时(TAI)之间会出现若干整数秒的差别。位于巴黎的国际地球自转事务中央局(IERS)负责决定何时加入闰秒。

### 夏日节约时间 DST

所谓「夏日节约时间」Daylight Saving Time (简称D.S.T.) ,是指在夏天太阳升起的比较早时,将时钟拨快一小时,以提早日光的使用,在英国则称为夏令时间(Summer Time)。这个构想于1784年由美国班杰明·富兰克林提出来,1915年德国成为第一个正式实施夏令日光节约时间的国家,以削减灯光照明和耗电开支。自此以后,全球以欧洲和北美为主的约70个国家都引用这个做法。目前被划分成两个时区的印度也正在商讨是否全国该统一实行夏令日光节约时间。欧洲手机上也有很多GSM系统的基地台,除了会传送当地时间外也包括夏令日光节约时间,做为手机的时间标准,使用者可以自行决定要开启或关闭。值得注意的是,某些国家有实施「夏日节约时间」的制度,出国时别忘了跟随当地习惯在表上调整一下,这可是机械表没有的功能设计哦！

## CST

而CST却同时可以代表如下 4 个不同的时区:
  
- Central Standard Time (USA) UT-6:00
- Central Standard Time (Australia) UT+9:30
- China Standard Time UT+8:00
- Cuba Standard Time UT-4:00

### RFC3339

RFC3339 比 ISO 8601 有一个很一个明显的限制, 这里提一下: ISO 允许 24 点,而 RFC3339 为了减少混淆, 限制小时必须在 0至 23 之间。23:59 过1分钟, 是第二天的00:00。
标准时间
本地时间只包括当前的时间,不包含任何时区信息。同一时刻,东八区的本地时间比零时区的本地时间快了8个小时。在不同时区之间交换时间数据,除了用纯数字的时间戳,还有一种更方便人类阅读的表示方式: 标准时间的偏移量表示方法。

RFC3339 详细定义了互联网上日期/时间的偏移量表示:

2017-12-08T00:00:00.00Z
这个代表了UTC时间的2017年12月08日零时

2017-12-08T00:08:00.00+08:00
这个代表了同一时刻的, 东八区北京时间 (CST) 表示的方法

上面两个时间的时间戳是等价的。两个的区别,就是在本地时间后面增加了时区信息。Z表示零时区。+08:00表示UTC时间增加8小时。

这种表示方式容易让人疑惑的点是从标准时间换算UTC时间。以CST转换UTC为例,没有看文档的情况下,根据 +08:00 的结尾,很容易根据直觉在本地时间再加上8小时。正确的计算方法是本地时间减去多增加的8小时。+08:00减去8小时才是UTC时间,-08:00加上8小时才是UTC时间。

参考资料一、linux调整系统时区/时间的方法(tzselect命令)

1) 找到相应的时区文件 /usr/share/zoneinfo/Asia/Shanghai

用这个文件替换当前的/etc/localtime文件。

2) 修改/etc/sysconfig/clock文件,修改为:

ZONE="Asia/Shanghai"
  
[color=red]UTC=true[/color]
  
ARC=false

3)
  
时间设定成2005年8月30日的命令如下:
  
# date -s 08/30/2005

将系统时间设定成下午6点40分0秒的命令如下。
  
# date -s 18:40:00

4)
  
同步BIOS时钟,强制把系统时间写入CMOS,命令如下:
  
# clock -w

5)重启apache。

参考资料二、
  
本文档解释了如何从linux下设置计算机的时钟,如何设置您的时区和其它与linux如何保存时间相关的材料。

您的计算机有两个时钟,一个是始终运行的、由电池供电的( 硬件的、BIOS或CMOS )时钟,另一个是由运行在您的计算机上的操作系统维护的( 系统 )时钟。硬件时钟通常只在操作系统启动时用来设置系统时钟,然后直到重启或关闭系统,由系统时钟来记录时间。在Linux 系统中,您可以选择用UTC/GMT 时间或本地时间来记录硬件时钟。推荐的选项是用UTC 记录,因为夏令时可以自动记录。使用UTC 记录硬件时钟的唯一不足是,如果您使用双系统,其它操作系统,如DOS 要求硬件时钟用本地时间设置,那么在那个操作系统里时间将是错误的。

设置时区:

Linux 下的时区是通过建立从/etc/localtime[1] 到/usr/share/zoneinfo [2] 目录下与您所在时区相符的文件的符号链结实现的。例如,由于我在南澳大利亚,/etc/localtime就是到 /usr/share/zoneinfo/Australia/South的符号链结。要建立这个链结,运行:

ln -sf ../usr/share/zoneinfo/your/zone /etc/localtime

替换your/zone 为形如Australia/NSW或Australia/Perth 的文件。看看/usr/share/zoneinfo目录都有什么时区。

[1] 这里假设/usr/share/zoneinfo 是到/etc/localtime 的链结的前提是Redhat Linux

[2] 在旧版本的系统里,您会发现使用/usr/lib/zoneinfo而不是/usr/share/zoneinfo。参考后面"一些应用程序中时间错误"。

设置UTC 或本地时间:

当Linux 启动时,一个启动脚本运行/sbin/hwclock 程序复制当前硬件时钟时间到系统时钟。hwclock 假定硬件时钟设置为本地时间,除非它使用了-utc 参数。在RedHat Linux下您不是编辑启动脚本,而是编辑/etc/sysconfig/clock 文件,相应的改变UTC 一行为UTC=true或UTC=false。

设置系统时钟:

在Linux 下设置系统时钟使用date命令。例如,设置当前时间和日期为July 31,11: 16pm,运行date 07312316 ( 注意这里的时间是24小时制) ；如果您想设置年份为1998, 应该运行date 073123161998 ；要是也想设置秒,运行date 07312316.30或date 073123161998.30。要查看Linux 当前本地时间,使用date,不带参数。

设置硬件时钟:

要设置硬件时钟,我喜欢的方式是首先设置系统时钟,然后设置硬件时钟为当前系统时钟时间,使用命令/sbin/hwclock -systohc (或 /sbin/hwclock -systohc -utc ) ,如果您使用UTC 保存硬件时钟) 。要查看当前硬件时钟的设置,不带参数运行hwclock 。如果硬件时钟是UTC 保存,而您想看相应的本地时间,运行/sbin/hwclock -utc 。

一些应用程序中时间错误:

如果一些应用程序,如date显示了正确的时间,而另一些则错误,而您运行着RedHat Linux 5.0/5.1,您很可能遇到了一个由于将时区信息从/usr/lib/zoneinfo 移动到/usr/share/zoneinfo 引起的bug 。修复的方法是建立一个从/usr/lib/zoneinfo 到/usr/share/zoneinfo 的符号链结:

ln -s ../share/zoneinfo /usr/lib/zoneinfo 。

小结:

*/etc/sysconfig/clock 设置硬件时钟,无论是用UTC 保存还是用本地时间保存
  
*建立/etc/localtime到/usr/share/zoneinfo/...的符号链结来设置时区
  
*运行date MMDDhhmm 来设置当前系统日期/ 时间
  
*运行/sbin/hwclock -systohc [-utc]来设置硬件时钟

其它有趣的注解:

Linux kernel总是按照从UTC 时间1970年1 月1 日午夜开始的秒数来储存和计算时间,无论您的硬件时钟是否用UTC 保存。转换到本地时间的工作是运行时完成的。这样做的一个妙处是,如果某人从不同的时区使用您的计算机,他可以设置时区环境变量, 所有的日期和时间可以按他的时区正确显示。

如果自UTC 1972年1 月1 日开始的秒数用保存为带正负号32位整数,如同在您的Linux/Intel 系统上一样,您的时钟将在2038年停止工作。Linux 没有Y2K 问题,但是确实存在2038年的问题。令人期望的是,那时我们都会使用64位系统来运行Linux 了。64位整数将使我们的时钟一直运行到大约2922.71亿年。

其它值得一看的程序:

- rdate ──从远程机器获得当前时间；可以用来设置系统时间
- xntpd ──类似rdata ,但是它是相当精确的,并且您需要有永久的网络连结xntpd 持续地运行,记录网络延时、时钟漂移等事件但是也有一个程序( ntpdate ) 包括在内,像rdate 一样设置当前时间。

附录一:  (推荐)
  
CST时区问题 在很多unix下用date命令都能看到当前的时区。很多unix下中国时区都是用CST表示的。但是这个表示方法非常不合理。因为CST同时代表了下面4个时区。

CST Central Standard Time (USA) UT-6:00
  
CST Central Standard Time (Australia) UT+9:30
  
CST China Standard Time UT+8:00
  
CST Cuba Standard Time UT-4:00

在unix下通过/etc/localtime这个硬连接指向的/usr/share/zoneinfo下的时区文件表示当前的真正时区。比如 /etc/localtime指向了/usr/share/zoneinfo/Asia/Shanghai这个文件的时候,CST就代表了中国标准时间。
  
但是很多语言的时间函数库根本不做这个判断,往往就是用一个独立的时区配置文件做时区关键字和GMT的转换。因此很多系统里面CST都变成了GMT-6,也就是美国中部时间。

在zope里面也是如此。而且很奇怪的是有的地方做了正确的判断,有的地方没做正确判断。
  
比如文件的最后修改时间就是错的,但是如果对一个页面做comment的时候,comment时间就是正确的。
  
修改Zope中DateTime\DateTime.py的定义为: 'cst':'GMT+8',就能够解决这个问题。
  
但是这样做就需要改代码,然后重新编译。
  
但既然CST这么不确定,就不能用。幸好有一个HKT,是表示香港的时间,也是东8区,这个没有错。托香港的福,就用这个好了。

附录二、
  
世界时区及时差计算
  
作者/来源:
  
2004-07-10 16:22 PM
  
责任编辑: 游乐儿

各地的标准时间为格林威治时间 (G.M.T) 加上 (+) 或减去 (-) 时区中所标的小时和分钟数时差。许多国家还采用夏令时 (DST) , 比如美国每年4月到9月实行夏令时,时间提前一个小时。

时差的计算方法: 两个时区标准时间 (即时区数) 相减就是时差,时区的数值大的时间早。比如中国是东八区(+8),美国东部是西五区(-5),两地的时差是13小时,北京比纽约要早13个小时；如果是美国实行夏令时的时期,相差12小时。

附: 世界标准时间表

标准时间代码
  
与GMT的偏移量
  
描述
  
NZDT
  
+13:00
  
新西兰夏令时
  
IDLE
  
+12:00
  
国际日期变更线,东边
  
NZST
  
+12:00
  
新西兰标准时间
  
NZT
  
+12:00
  
新西兰时间
  
AESST
  
+11:00
  
澳大利亚东部夏时制
  
CST(ACSST)
  
+10:30
  
中澳大利亚标准时间
  
CADT
  
+10:30
  
中澳大利亚夏时制
  
SADT
  
+10:30
  
南澳大利亚夏时制
  
EST(EAST)
  
+10:00
  
东澳大利亚标准时间
  
GST
  
+10:00
  
关岛标准时间
  
LIGT
  
+10:00
  
澳大利亚墨尔本时间
  
CAST
  
+9:30
  
中澳大利亚标准时间
  
SAT(SAST)
  
+9:30
  
南澳大利亚标准时间
  
WDT(AWSST)
  
+9:00
  
澳大利亚西部标准夏令时
  
JST
  
+9:00
  
日本标准时间,(USSR Zone 8)
  
KST
  
+9:00
  
韩国标准时间
  
MT
  
+8:30
  
毛里求斯时间
  
WST(AWST)
  
+8:00
  
澳大利亚西部标准时间
  
CCT
  
+8:00
  
中国沿海时间(北京时间)
  
JT
  
+7:30
  
爪哇时间
  
IT
  
+3:30
  
伊朗时间
  
BT
  
+3:00
  
巴格达时间
  
EETDST
  
+3:00
  
东欧夏时制
  
CETDST
  
+2:00
  
中欧夏时制
  
EET
  
+2:00
  
东欧,(USSR Zone 1)
  
FWT
  
+2:00
  
法国冬时制
  
IST
  
+2:00
  
以色列标准时间
  
MEST
  
+2:00
  
中欧夏时制
  
METDST
  
+2:00
  
中欧白昼时间
  
SST
  
+2:00
  
瑞典夏时制
  
BST
  
+1:00
  
英国夏时制
  
CET
  
+1:00
  
中欧时间
  
DNT
  
+1:00
  
Dansk Normal Tid
  
FST
  
+1:00
  
法国夏时制
  
MET
  
+1:00
  
中欧时间
  
MEWT
  
+1:00
  
中欧冬时制
  
MEZ
  
+1:00
  
中欧时区
  
NOR
  
+1:00
  
挪威标准时间
  
SET
  
+1:00
  
Seychelles Time
  
SWT
  
+1:00
  
瑞典冬时制
  
WETDST
  
+1:00
  
西欧光照利用时间 (夏时制)
  
GMT
  
0:00
  
格林威治标准时间
  
WET
  
0:00
  
西欧
  
WAT
  
-1:00
  
西非时间
  
NDT
  
-2:30
  
纽芬兰 (新大陆) 白昼时间
  
ADT
  
-03:00
  
大西洋白昼时间
  
NFT
  
-3:30
  
纽芬兰 (新大陆) 标准时间
  
NST
  
-3:30
  
纽芬兰 (新大陆) 标准时间
  
AST
  
-4:00
  
大西洋标准时间 (加拿大)
  
## EDT (美国)东部夏令时
  
-4:00

## CDT (美国)中部夏令时
  
-5:00

## PT

UTC/GMT -7:00小时

EST
  
-5:00
  
 (美国)东部标准时间
  
CST
  
-6:00
  
 (美国)中部标准时间
  
MDT
  
-6:00
  
 (美国)山地夏令时
  
MST
  
-7:00
  
 (美国)山地标准时间
  
PDT
  
-7:00
  
 (美国)太平洋夏令时
  
PST
  
-8:00
  
 (美国)太平洋标准时间
  
YDT
  
-8:00
  
Yukon夏令时
  
HDT
  
-9:00
  
夏威仪/阿拉斯加白昼时间
  
YST
  
-9:00
  
Yukon标准时
  
AHST
  
-10:00
  
夏威仪-阿拉斯加标准时间
  
CAT
  
-10:00
  
中阿拉斯加时间
  
NT
  
-11:00
  
州时间 (Nome Time)
  
IDLW
  
-12:00
  
国际日期变更线,西边

[http://blog.csdn.net/wb96a1007/article/details/7945021](http://blog.csdn.net/wb96a1007/article/details/7945021)
  
[http://www.91linux.com/html/2014/Linux_rumen_0127/5145.html](http://www.91linux.com/html/2014/Linux_rumen_0127/5145.html)
  
[https://blog.csdn.net/webcainiao/article/details/4018761](https://blog.csdn.net/webcainiao/article/details/4018761)


## timezone PDT,PST,UTC GMT EST CST

什么是PDT,PST美国时间

作者: YoungKing 日期: 2009年04月18日 发表评论 (0)查看评论

经常在网上看到"在09-4-18， PDT 上午10:00 "等信息，那么什么是PDT呢？

PDT是Pacific Daylight Time太平洋夏季时间。美国西海岸(旧金山 洛杉矶 西雅图 波特兰)在夏时制时用这一时间。

美国夏季始于每年4月的第1个周日，止于每年10月的最后一个周日。夏令时比正常时间早一小时。

相对应的是PST , Pacific Standard Time 。 夏时制结束后就是PST。

PST是太平洋标准时间 (西八区) ，与北京时间 (东八区) 时差-16个小时，也就是北京时间减去16就是PST时间。而PDT比PST早1个小时，就是说PDT与北京时间时差为-15小时。

美国横跨西五区至西十区，共六个时区。每个时区对应一个标准时间，从东向西分别为东部时间(EST)(西五区时间)、中部时间(CST)(西六区时间)、山地时间(MST)(西七区时间)、太平洋时间(西部时间)(PST)(西八区时间)、阿拉斯加时间(AKST)(西九区时间)和夏威夷时间(HST)(西十区时间)，按照"东早西晚"的规律，各递减一小时。

美国标准时间 与北京时间时差(小时)

HST -18

AKST -17

PST -16

MST -15

CST -14

EST -13

夏季始于每年4月的第1个周日，止于每年10月的最后一个周日。也称为DST: Daylight Saving Time 。。

美国夏季时间 与北京时间时差(小时)

HDT -17

AKDT -16

PDT -15

MDT -14

CDT -13

EDT -12

简介
UTC GMT EST PST 各种时间标准傻傻分不清

GMT (Greenwich Mean Time) 的缩写，指的是皇家格林威治天文台的标准时间，称作格林威治时间，因为本初子午线通过此地区，因此也称为世界标准时间。
然而地球的自转不是完全规律的，而且正逐渐减慢，因此自1924年开始，格林威治时间(GMT)已经不再被视为标准时间，
取而代之的是"世界协调时间" (UTC: Coordinated Universal Time)

UTC 协调世界时 (Coordinated Universal Time) 是最主要的世界时间标准，其以原子时秒长为基础，在时刻上尽量接近于格林尼治标准时间。UTC 是一个标准，而不是一个时区

CST 北京时间，China Standard Time，中国标准时间，是中国的标准时间。在时区划分上，属东八区，比协调世界时早8小时，记为UTC+8

EST CST 是众多时区中的一种时区

下面是全球热门时区及其缩写的网站

缩写    全称    中文名称    类型    UTC 偏移量
+03    +03        -    UTC +03:00
+04    +04        -    UTC +04:00
+05    +05        -    UTC +05:00
+0530    +0530        -    UTC +05:30
+06    +06        -    UTC +06:00
ACDT    Australian Central Daylight Time    澳大利亚中部夏令时    夏令时    UTC +10:30
ACST    Australian Central Standard Time    澳大利亚中部标准时间    -    UTC +09:30
ACT    Acre Time    阿卡时间    -    UTC -05:00
ACWST    Australian Central Western Standard Time    澳大利亚中西部标准时间    -    UTC +08:45
ADT    Atlantic Daylight Time    大西洋夏令时间    夏令时    UTC -03:00
AEDT    Australian Eastern Daylight Time    澳大利亚东部夏令时    夏令时    UTC +11:00
AEST    Australian Eastern Standard Time    澳大利亚东部标准时间    -    UTC +10:00
AFT    Afghanistan Time    阿富汗时间    -    UTC +04:30
AKDT    Alaska Daylight Time    阿拉斯加夏令时    夏令时    UTC -08:00
AKST    Alaska Standard Time    阿拉斯加标准时间    -    UTC -09:00
AMST    Amazon Summer Time    亚马逊夏令时    夏令时    UTC -03:00
AMT    Amazon Time    亚马逊时间    -    UTC -04:00
ART    Argentina Time    阿根廷时间    -    UTC -03:00
AST    Arabia Standard Time    阿拉伯标准时间    -    UTC +03:00
AST    Atlantic Standard Time    大西洋标准时间    -    UTC -04:00
AWST    Australian Western Standard Time    澳大利亚西部标准时间    -    UTC +08:00
AZOST    Azores Summer Time    亚速尔群岛夏令时    夏令时    UTC -00:00
AZOT    Azores Time    亚速尔群岛时间    -    UTC -01:00
BOT    Bolivia Time    玻利维亚时间    -    UTC -04:00
BRST    Brasília Summer Time    巴西利亚夏令时    夏令时    UTC -02:00
BRT    Brasília Time    巴西利亚时间    -    UTC -03:00
BST    British Summer Time    英国夏令时间    夏令时    UTC +01:00
BTT    Bhutan Time    不丹时间    -    UTC +06:00
CAT    Central Africa Time    中非时间    -    UTC +02:00
CDT    Central Daylight Time    中部夏令时间    夏令时    UTC -05:00
CDT    Cuba Daylight Time    古巴夏令时    夏令时    UTC -04:00
CEST    Central European Summer Time    欧洲中部夏令时间    夏令时    UTC +02:00
CET    Central European Time    欧洲中部时间    -    UTC +01:00
CHADT    Chatham Island Daylight Time    查塔姆岛夏令时    夏令时    UTC +13:45
CHAST    Chatham Island Standard Time    查塔姆岛标准时间    -    UTC +12:45
CHOST    Choibalsan Summer Time    乔巴山夏令时    夏令时    UTC +09:00
CHOT    Choibalsan Time    乔巴山时间    -    UTC +08:00
CHUT    Chuuk Time    丘克时间    -    UTC +10:00
CKT    Cook Island Time    库克群岛时间    -    UTC -10:00
CLST    Chile Summer Time    智利夏令时    夏令时    UTC -03:00
CLT    Chile Standard Time    智利标准时间    -    UTC -04:00
CST    Central Standard Time    中部标准时间    -    UTC -06:00
CST    China Standard Time    中国标准时间    -    UTC +08:00
CST    Cuba Standard Time    古巴标准时间    -    UTC -05:00
ChST    Chamorro Standard Time    查莫罗标准时间    -    UTC +10:00
EASST    Easter Island Summer Time    复活岛夏令时    夏令时    UTC -05:00
EAST    Easter Island Standard Time    复活节岛标准时间    -    UTC -06:00
EAT    Eastern Africa Time    非洲东部时间    -    UTC +03:00
ECT    Ecuador Time    厄瓜多尔时间    -    UTC -05:00
EDT    Eastern Daylight Time    东部夏令时间    夏令时    UTC -04:00
EEST    Eastern European Summer Time    东欧夏令时    夏令时    UTC +03:00
EET    Eastern European Time    东欧时间    -    UTC +02:00
EST    Eastern Standard Time    东部标准时间    -    UTC -05:00
FKST    Falkland Islands Summer Time    福克兰群岛夏令时    -    UTC -03:00
GFT    French Guiana Time    法属圭亚那时间    -    UTC -03:00
GILT    Gilbert Island Time    吉尔伯特群岛时间    -    UTC +12:00
GMT    Greenwich Mean Time    格林威治标准时间    -    UTC -00:00
GST    Gulf Standard Time    海湾标准时间    -    UTC +04:00
HKT    Hong Kong Time    香港时间    -    UTC +08:00
HST    Hawaii Standard Time    夏威夷标准时间    -    UTC -10:00
ICT    Indochina Time    印度支那时间    -    UTC +07:00
IDT    Israel Daylight Time    以色列夏令时    夏令时    UTC +03:00
IRDT    Iran Daylight Time    伊朗夏令时    夏令时    UTC +04:30
IRST    Iran Standard Time    伊朗标准时间    -    UTC +03:30
IST    India Standard Time    印度标准时间    -    UTC +05:30
IST    Irish Standard Time    爱尔兰标准时间    夏令时    UTC +01:00
IST    Israel Standard Time    以色列标准时间    -    UTC +02:00
JST    Japan Standard Time    日本标准时间    -    UTC +09:00
KOST    Kosrae Time    科斯雷时间    -    UTC +11:00
KST    Korea Standard Time    韩国标准时间    -    UTC +08:30
LINT    Line Islands Time    莱恩群岛时间    -    UTC +14:00
MDT    Mountain Daylight Time    山区夏令时    夏令时    UTC -06:00
MHT    Marshall Islands Time    马绍尔群岛时间    -    UTC +12:00
MSK    Moscow Standard Time    莫斯科标准时间    -    UTC +03:00
MST    Mountain Standard Time    山地标准时间    -    UTC -07:00
MYT    Malaysia Time    马来西亚时间    -    UTC +08:00
NDT    Newfoundland Daylight Time    纽芬兰夏令时    夏令时    UTC -02:30
NPT    Nepal Time    尼泊尔时间    -    UTC +05:45
NST    Newfoundland Standard Time    纽芬兰标准时间    -    UTC -03:30
NUT    Niue Time    纽埃时间    -    UTC -11:00
NZDT    New Zealand Daylight Time    新西兰夏令时    夏令时    UTC +13:00
NZST    New Zealand Standard Time    新西兰标准时间    -    UTC +12:00
PDT    Pacific Daylight Time    太平洋夏令时    夏令时    UTC -07:00
PET    Peru Time    秘鲁时间    -    UTC -05:00
PGT    Papua New Guinea Time    巴布亚新几内亚时间    -    UTC +10:00
PHT    Philippine Time    菲律宾时间    -    UTC +08:00
PKT    Pakistan Standard Time    巴基斯坦标准时间    -    UTC +05:00
PONT    Pohnpei Standard Time    波纳佩标准时间    -    UTC +11:00
PST    Pacific Standard Time    太平洋标准时间    -    UTC -08:00
SAST    South Africa Standard Time    南非标准时间    -    UTC +02:00
SBT    Solomon Islands Time    所罗门群岛时间    -    UTC +11:00
SGT    Singapore Time    新加坡时间    -    UTC +08:00
SRT    Suriname Time    苏里南时间    -    UTC -03:00
SST    Samoa Standard Time    萨摩亚标准时间    -    UTC -11:00
TAHT    Tahiti Time    塔希提岛时间    -    UTC -10:00
TLT    East Timor Time    东帝汶时间    -    UTC +09:00
TVT    Tuvalu Time    图瓦卢时间    -    UTC +12:00
ULAST    Ulaanbaatar Summer Time    乌兰巴托夏令时    夏令时    UTC +09:00
ULAT    Ulaanbaatar Time    乌兰巴托时间    -    UTC +08:00
UYST    Uruguay Summer Time    乌拉圭夏令时    夏令时    UTC -02:00
UYT    Uruguay Time    乌拉圭时间    -    UTC -03:00
VET    Venezuelan Standard Time    委内瑞拉标准时间    -    UTC -04:00
WAST    West Africa Summer Time    西非夏令时    夏令时    UTC +02:00
WAT    West Africa Time    西非时间    -    UTC +01:00
WEST    Western European Summer Time    西欧夏令时间    夏令时    UTC +01:00
WET    Western European Time    西欧时间    -    UTC -00:00
WIB    Western Indonesian Time    印尼西部时间    -    UTC +07:00
WIT    Eastern Indonesian Time    印度尼西亚东部时间    -    UTC +09:00
WITA    Central Indonesian Time    印度尼西亚中部时间    -    UTC +08:00

---

https://blog.csdn.net/x356982611/article/details/90296245
