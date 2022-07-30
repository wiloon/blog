---
title: 第一届黑客信息战 MIT CTF 2011记录
author: "-"
date: 2012-03-06T12:57:43+00:00
url: /?p=2525
categories:
  - Linux
tags:
  - reprint
---
## 第一届黑客信息战 MIT CTF 2011记录

这个是前两天我朋友 dcluo 在 MIT(麻省理工学院) 参加的一个黑客竞赛的实战记录

分享给大家看看 感受一下国外的技术竞赛魅力

————————————————————————

- 第一届 MIT CTF 2011 信息战随笔 –

此次经历，值得记录

(我尽量写的详细，希望各大学校组织效仿这类比赛)

前言:

事情追溯到几个月前在 hackathon 有幸认识了一位MIT 计算机女强人 haoqi 同学。

(hacakthon是微软举办的一个过夜的"搞破坏者"的集会。)在大约凌晨2点左右。。

我和她都被微软强行推荐的 Windows 7 Phone 寂寞无聊的不行。

我突然对她说，你对网络入侵感兴趣么？

一下子，一拍即合。于是引导了今天和昨天 20个小时的入侵攻防信息战模拟。

比赛名称: MIT CTF 2011

时间: 4月2~3日 早8: 30 – 晚9:00点

地点: MIT

人物: 韩国网安内核牛+haoqi+我 + 其他12个组 (～45人)

比赛规格:

• 13组小队 (MIT，BU，UMASS，NE…)

• 一个组一个VM (ubuntu 10.10 + 最新apache+MySQL+wordpress) 分别运行在同一个虚拟机服务器上但是不同IP和Domain。

• 每个组一个SWITCH BOX 和 名为 ctfuser 的用户权限(ssh) 和三个密码 (ssh+wordpress+评分页密码)

• WordPress 每随机一段时间会要求安装一个plugin。

• 每天可以有一个snapshot和三次全盘恢复机会。

任务目标:

1. 获取其他组的flag (128位String) 这个flag 散落在VM的各个角落 (文件或数据库里)

2. 保护自己的wordpress 和 plugins 都能正常运行，保护自己的flag 没有被更改过

3. flag 每10分钟改变一次， 有可能会改变位置 (裁判是root 权限)

除了ddos 和 spoofing 其余手段的均可

评分标准:

• Availability (可以fetch wordpress的xmlrc 以及plugin的正常工作)

• Confidentiality (被别人提交flag的数量)

• Integrity (flag被人改的次数)

• Offense (提交旗子百分比)

• 以上是基于每分钟随即次数刷新计算的

介绍差不多了，下面开始！

———————————————————-

DAY1

风和日丽的星期六早上，我7点的闹钟就把3点才睡的可爱室友们吵醒，

收拾设备赶去参加了这次打着 Lincoln Laboratory 多名科学家名义下的比赛。

下了出租车，快步跑到了计算机房就被MIT的设备震惊了。

大概3百平方米的房间里，散落着20面三个客户机一桌子。

环绕房间一周的是8台180寸(目测)投影仪，一台为比赛拆包的ESX 服务器和13包崭的新Switchs。

身为第一个抵达现场的，我优先选了一个角落的一个桌子。

这个角度，我可以看到别的组的屏幕(邪恶)，不过事实证明信息战的时候根本没时间看(= =!)此处省略一万字感叹。

我笔记本6个terminal ssh待命 + 网本wireshark 嗅开始。 8: 30所有虚拟机上线。

8: 31 @ 4月2日

6个terminal 里 一顿回车，复制粘贴了10位随机字符的密码，连入！

第一件事: 加固！scp上传了已经事先准备好了的加固script 后， ./install.sh ！

由于很多大牛都问我怎么加固的这里简单介绍下:  加固脚本分为4个部分。

Mod_security , htaccess , chown 和 cleanup。

加了apache mod 后大部分的侵略性数据包都能比较轻松的过滤掉

(我们升级了下，所有get 和 post 含有union, concat, 3,4,5 等都丢包)。

Htaccess 一些重要www目录，例如 /wp-admin. 关于chown， 我们把所有 /var/www/ 权限扔到了一个新建plug-in用户。

之后安装了blocker.php 和ssh iptable设置，

sudo rm /etc/apache2/conf.d/javascript-common.confsudo 和rm /etc/apache2/conf.d/phpmyadmin.conf (嘿嘿嘿。。)

不到一分钟，执行完毕。 我们当然需要root 才爽嘛。这件事自然交给了韩国网安内核牛，一回车，root权限拿到。

(有兴趣的同学可以看看内核牛的CV。2年韩国情报员；MIT GPA 5.0/5.0 ；Microsoft高薪聘请他拒绝了三次，

最后邀请到win 7 开发团队，做了没多久他还是觉得没意思。再Ps: 打听到了win7源码8G 需要16个小时compile)

坏笑着apache2/access.log 里面各种各样被拒绝的变种数据包，随便粘几个地址，节省我好多vim plugin的时间！

前文我提到了我同时用6个terminals，我说下每个terminals的工作:

2个terminal负责 apache 和 inode 文件创建修改 log， 1个(半屏)负责读php 代码找漏洞，另外三个nc 端口待命。

正当坏笑没有任何非法连接能进入到系统的时候，并且读log利用这些链接乱注入别人的时候，

抬头看到8个投影射出的评分板，我们的分数从第一在往下高速下 滑！！Availability！！

此时比赛已经进行了3个小时，评委耐不住好奇，跑到我们面前问为什么不能正常fetch 检查网站在线。

原因很简单: 我们设置的有点过分了。

根据我们的设置，

评分的python脚本发送数据包的速度> 5个数据包/s 所以每次批量检查运行情况，我们服务器会他们的ip链接进行50秒的静默。

其中，正常的apache访问，我们加了个n 来防护xml 相关攻击。

由于裁判的疏忽，py的指针读取第一行发现是空行，以为服务器不在线。

在那半个小时之后，我们才迅速trouble shoot 自己的配置来满足裁判的评分接口。

来回来去跑到控制塔向裁判complain 无望，我们的分数已经跌了81% 顺利获得了另一个第一: 倒数第一！(低于倒数第二12%)

接下来是12: 00-1: 00的lunch break， 此时韩国牛，haoqi还有我都一脸忧郁。

12: 03 @ 4月2日

盯着评分版，愤愤不平的和组员们去了student union吃饭。 有心无心的嚼着饭，分析着利弊。

我们的除了availability 其余项目都第一或第二。但是我们已经已经有了貌似无望回天的比例丢失。

1: 01 @ 4月2日

拖着平平的脚步回到赛场，坐下。

挠着已经麻木的头，分析自己的优势: 没有一个队伍得到或者更改了我们的flag。

毫不客气的拿着他们的log， 我们开始利用他们的提交肆虐攻击其他服务器。

经过了大概一个小时，我们获得了大概4个站的eval 和3个站的 exec。

韩国牛迅速写了个py收集，我负责迅速编写反弹shell+找php漏洞， haoqi同学负责提交 flag。

这里给下例子flag 长什么样:

lfTogfKGCdnt5pEACWISafVsyqAuXYQEmfMbaBQc0QnuoYNrWZQ0aWkSFzqcyrb8ViGds3QebrBCjWMIoUQjkNWcMY7vE8sVwGbG7glOy1IIuBY2UWXQbaLPk3tQ8u8b

tTc1pkcVTwYDfTIQuCCTonCq84AEKOhsLVXqlYj5rbTtgZpHqVjlATE7qo4gTg6DiO8X0543AuNXGjF8WtcqKWQ9yVXgth6tzO3lJVa9sMqeXD03UyQC5R5yuNROgDhO

8fMDJPTZaQn1BK026Xf4vXgiYKWvaj6QwVIuQ58tzgqnuH3sFrKnCNMwYFIfJ35jP8nVtXytjf73hZksIPgObCBGWLfXEE1YAMRUCgtAaBNiXMBfThUKX4yl68vESUEU

RHoXzhQwhuaOQGmdaSWnOb0fCwNpTM7YgMwXzKUoQRaAeLUfBF1JV19oPj5XV1wXDD4D2nBAYpCNKkCecswHEOMHikmU5OCYvB90vuer2d4yKFpqNqfzJlIemVQ6yFs5

以上是4个 flag的样子。 提交的网页也很是变态，是个https的链接，我一直没找到合理的脚本接口。

这里感谢Anthr@x牛的hint， 用php 成功写了个较高效率的提交脚本。

此时的我们，韩国牛疯狂的在打键盘攻击， 我疯狂的在vim /eval ， 和haoqi疯狂的提交。

我们在下午场提交了 70-80多个flag 并保持着唯一的 100% Confidentiality。

让一个平均值增长是个艰苦的过程，一直到7: 00PM我们排名8/13。

所有虚拟机暂停！也许是觉得不公平吧， 虚拟机虽然停一个小时逼我们去吃饭，但是我们没有！

我和韩国牛在埋头写代码和攻击脚本，此时的haoqi 贤惠的帮我们去买饭。

20: 02 @ 4月2日

边吃着盒饭，边敲着键盘的我等待着服务器恢复。

Ssh一通，我们顺利的吧脚本传上去，

顺带着把先前A牛给我的rips 传到www (这里介绍个命令 grep –ir "eval(" .所以rips用处一般)。

这时的别的队，很多已经被迫下线甚至删干净了(密码都一样绝对悲剧!)。

看到很多队伍跑到主机塔那里，管裁判要恢复机会，我们的脸上已经都露出了很坏的笑容。

看着别的队伍无助的链接请求，身为唯一只有三个人团队的我们已经挤进了前三名。

一个小时很快就过去了。 9: 00 我们带着激动和希望回家了。

第一天入侵总结:

Eval(), exec() 是基本利用，但效率才是输赢关键。

根据不同的漏洞，能在他们发现并打补丁前迅速做出同时或短时间相继攻击其余12台服务器的脚本或代码。

这里说下，别的队 伍也不是卖白菜的。也是设置要多变态有多变态。

有的队伍设置了个https 在他们的服务器，有的队伍的网页域名直接转向到某ip地址，

有的队伍索性屏蔽了除了裁判所有其他人的ip (后被认为作弊，但没扣分)，

更有恶心的队伍直接把所有东西跳转到当时排名第一的队伍。。。

大家形形色色的信息攻击虽然trivial但是也需要很多技巧。

大家都是在不停刷新log， 每看到一个链接，大家都是迅速切断。

在那1-2秒里，我们必须得做到提权，或者偷旗子。

比赛无时无刻都体现出能用好一个editor的重要性。

这里小d敬告读者，emacs 或者 vim 选一个！用好它，造福你一生！

———————————————————-

DAY2
  
依旧风和日丽，7点闹钟。

一脸的懒散，蹒跚到i7前打开qq，看到了各位大牛的各种留言，马上得唆起昨天惊心动魄的信息战。

迅速的跑去刷完牙，继续和牛们各种扯淡。殊不知在我早上沾沾自喜的时候，排名后面的队伍都是不眠夜。

8: 49 @ 4月3日

比赛开始的晚了一点，因为有几个队伍已经没有信心主动退场了。

Well， 我们还是等了他们。 这时的我们做下资源清点: 我们手上有3台webshell， 4台root 。

还是惯例性连过去偷旗子。 这里要表扬下team6， 他们把他们收集到的旗子都很整齐的存在他们系统里。

帮我们节省了很多时间。慢慢的大概10: 30左右，我们脚步放慢了，也不紧张了。以为比赛已经进入了僵局。

此时我们还保持着晋升的第二。这时我们的队长收到了一封social engineering的邮件。

我们可爱的队长，就这么被社工了。其他队伍真是yd啊！

跑去注册了<http://mitctf-2011.wikispaces.com/grading-Key> 做的和官方网站一模一样，

但是多了个警示: 所有的队伍请检查ssh key是不是和这个相等，

ssh-rsa

AAAAB3NzaC1yc2EAAAABIwAAAQEAtAxPlNf+AWFr3Fn/lN9g4XBkxN7JX3YxZwxYMGixEj0iGSq3B0Lx8tgENISh6PEF6xzZoCv2btQT1Sarf7LLtHygjhGss

/6wxX+uhsbrGAEkVcuO3ESxZPesvgf1KAZ0jW5ct7VW5B7u4zL1aC2hL5UQ4hHGIR2CFHKNl9f8wsL9XORfMPBN44Qfyjjhv9qjMx69kxc+wA9jdwsVUTLhgHmRtlubMIMXrfwICObsAEyjg

/DRAH78KOZrra9RFwovT09BX07EsWN0kNeie4Off2GFAAmR+cgP0NseCTcP2Jb

/yNt7PsoAwPIOp4sYme+t3EUBOd+ooOBRRxm4v80YKQ==timleek@thunk.local

韩国牛看着public key 想都没想，就发现不对了。此处省略50字。

几乎是同时发生的，我刚打完ls， 返回路径没了。cd .. 路径没了！pwd 没了！！我们的VM被人整个格式化了。

一切都发生在不到20秒里。脑子一下空白，紧张的跑到控制台申请恢复。

此时看到隔壁桌的几个人在邪恶的各种偷笑。 心里气愤和怨恨！

Ssh进去后，镇定一下，修改root密码，检查iptable， 只允许我们组员的ssh链接。

这时大概1分钟过去了。Haoqi告诉我，网站被改成了一个youtube视频！命令行里再一执行，又被一锅端了。

Pipe broken! 服务器第二次被删空。这下好，我们都被杀红了眼，第三次跑到了服务台，申请了恢复和3分钟服务器执行时间。

很明显我们的假设是错的。就这样，我们守着个空VM唯一能做的就是metasploits别的服务器。

基本无望，因为貌似别的服务器也都陷入了同样的窘境。

Team7 是team7!! 本来垫底的他们一直赶超取代了我们的第二。

不久之后，12: 00午餐时间到。

12: 11 @ 4月3日

脑子一团浆糊的我，还有一脸无奈的韩国牛分析着入侵的原因。

Iptable屏蔽了怎么还是被入侵了？难道裁判被入侵了？

啃着subway，默念着，希望能保住第三。

13: XX@ 4月3日

此时时间已经不重要了，我们唯一能做的，就是尽一切可能攻击别的团队。

下载来metasploits到我的笔记本，开始尝试各种payload，面对新版本或者和我们一样的系统统统无效。

过了一阵子，team7上升的强势已经注定了我们败下第三。经过检测发现只有两台VM服务器在运行。

一台apache stop了，其中一台就是攻击我们的人。

时间一下子充裕起来，回想下失败在哪里。

绞尽脑汁也想不出来，于是乎打开了wine 玩起了cs消磨时间，加入了寂寞等待比赛结束的队列。

省略1万字的时间过去了，我们的服务器已经关机了7个小时的无奈，和赞叹技术不如人。

毕竟，连入侵手法我们都不知道！！

19: XX @ 4月3日

经过我们强烈的要求，要求第七组 (UMass) 公布入侵我们幻想的无敌服务器思路时候，

我们才了解到，他们全组5个人一晚上没有回家。昼夜睡在了MIT分析所有plugin。

他们漏洞的利用，我虽然第一时间看到了，可是完全没有当回事。

因为一眼望过去，复杂程度不是20个小时的比赛所能完全利用的。

正因为这样，当有付出的时候 才有回报。他们的付出让他们从倒数第一，杀到了第二名。

他们把数据包巧妙的修改，cookie base64加密，然后利用源程序解密，巧妙的绕过了我们所有的base64, eval检测。

他们不惜一切代价，搞到了XXX提权，我们的内核牛都没打的补丁。

10分钟里就把除apache不运行的服务器全都ko掉。

攻击的深度，速度，和准度无不映射出来，我熟睡时他们下血本的邪恶的阴谋！

我们灰溜溜的离开了这个无硝烟战场。

第二天入侵总结:

有付出就有回报。垫底总有翻身的一天！坚持不懈，就会看到光荣榜上你的名字。

笔者: dcluo

提供: VM 源代码，plugin 打包， 攻防wiki

未校对 2011年4月4日 凌晨1: 40分

—————————————————————

VM:

<http://mitctf2011.wikispaces.com/Competition+VM>

说明下 我和 dcluo 测试过

貌似被写死了平台只能在ubuntu的VMPlayer上启动

plugin打包:

<http://u.115.com/file/f47ab66eae>

攻防wiki:

<http://mitctf2011.wikispaces.com/MIT+CTF+external+links+for+self-study>

来源: <http://hi.baidu.com/hackercasper/blog/item/1e165434c681340490ef398c.html>
