---
title: parted gdisk fdisk
author: wiloon
type: post
date: 2018-05-10T06:15:35+00:00
url: /?p=12223
categories:
  - Uncategorized

---
http://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi\_linux\_039\_fdisk\_gdisk_parted.html

1 2种分区结构简介
  
MBR分区

硬盘主引导记录MBR由4个部分组成
  
主引导程序（偏移地址0000H&#8211;0088H），它负责从活动分区中装载，并运行系统引导程序。
  
出错信息数据区，偏移地址0089H&#8211;00E1H为出错信息，00E2H&#8211;01BDH全为0字节。
  
分区表（DPT,Disk Partition Table）含4个分区项，偏移地
  
址01BEH&#8211;01FDH,每个分区表项长16个字节，共64字节为分区项1、分区项2、分区项3、分区项4
  
结束标志字，偏移地址01FE&#8211;01FF的2个字节值为结束标志55AA
  
GPT分区

GPT:GUID（Globals Unique Identifiers） partitiontable 支持128个分区，使用64位，支持8Z（512Byte/block ）64Z （ 4096Byte/block）
  
使用128位UUID(Universally Unique Identifier) 表示磁盘和分区 GPT分区表自动备份在头和尾两份，并有CRC校验位
  
UEFI (统一扩展固件接口)硬件支持GPT，使操作系统启动
  
2 fdisk的使用
  
2.1 fdisk命令的基础
  
复制代码
  
[root@centos7 mnt]$ dd if=/dev/fdisk /dev/sdb
  
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
  
Be careful before using the write command.

Device does not contain a recognized partition table
  
Building a new DOS disklabel with disk identifier 0xc0e6470d.

Command (m for help): m
  
Command action
     
a toggle a bootable flag # 切换可启动标志
     
b edit bsd disklabel　　　　　　　　　　　　　　　　　　 # 编辑磁盘标记
     
c toggle the dos compatibility flag　　　　　　　　　　　　　　 # 切换dos兼容标志
     
d delete a partition　　　　　　　　　　　　　　　　　　　　　　　 # 删除一个分区
     
g create a new empty GPT partition table 　　 # 创建一个空的GPT分区表
     
G create an IRIX (SGI) partition table 　　 # 创建一个IRIX分区表
     
l list known partition types　　　　　　　　　　　　　　　　　　　# 列出已知的分区类型
     
m print this menu　　　　　　　　　　　　　　　　　　　　　　　　　　# 打印菜单　　　　　　　　　　　　　　　　　　　
     
n add a new partition # 添加一个分区
     
o create a new empty DOS partition table # 创建一个空的DOS分区表
     
p print the partition table # 打印分区表
     
q quit without saving changes # 退出不保存
     
s create a new empty Sun disklabel # 创建一个空的sun磁盘标签
     
t change a partition&#8217;s system id # 改变一个分区的类型
     
u change display/entry units # 改变显示的单位
     
v verify the partition table # 验证分区表
     
w write table to disk and exit # 写分区表并退出
     
x extra functionality (experts only) # 高级功能

Command (m for help):
  
复制代码
  
2.2 fdisk实战
  
例子： 使用fdisk工具给/dev/sdb（100G）分区满足下面几个要求

3个主分区一个扩展分区
  
/dev/sdb1分区类型为Linux LVM，大小为30G
  
/dev/sdb2分区类型为swap，大小为20G
  
/dev/sdb3分区类型为Linux， 大小为10G
  
/dev/sdb5分区类型为linux,大小为10G
  
保留40G留作后用
   
View Code
  
3 gdisk的使用
  
3.1 gdisk的命令基础
  
复制代码
  
[root@centos7 mnt]$ gdisk /dev/sdb
  
GPT fdisk (gdisk) version 0.8.6

Partition table scan:
    
MBR: MBR only
    
BSD: not present
    
APM: not present
    
GPT: not present

* * *

Found invalid GPT and valid MBR; converting MBR to GPT format.
  
THIS OPERATION IS POTENTIALLY DESTRUCTIVE! Exit by typing &#8216;q&#8217; if
  
you don&#8217;t want to convert your MBR partitions to GPT format!

* * *

Command (? for help): ?
  
b back up GPT data to a file # 备份一个gpt数据到文件
  
c change a partition&#8217;s name # 改变分区名
  
d delete a partition # 删除一个分区
  
i show detailed information on a partition # 显示一个分区的详细信息
  
l list known partition types # 列出已知的分区类型
  
n add a new partition # 添加一个新的分区
  
o create a new empty GUID partition table (GPT) # 创建一个空的GUID分区表
  
p print the partition table # 打印分区表
  
q quit without saving changes # 退出不保存
  
r recovery and transformation options (experts only) # 专家模式
  
s sort partitions # 排序分区
  
t change a partition&#8217;s type code # 改变分区类型
  
v verify disk # 验证磁盘
  
w write table to disk and exit # 写磁盘并退出
  
x extra functionality (experts only) # 额外功能（专家模式）
  
? print this menu # 打印菜单

Command (? for help):
  
复制代码

3.2gdisk实战
  
例子： 使用gdisk工具给/dev/sdb（100G）分区满足下面几个要求

GPT分区
  
/dev/sdb1分区类型为Linux LVM，大小为30G
  
/dev/sdb2分区类型为swap，大小为20G
  
/dev/sdb3分区类型为Linux， 大小为10G
  
/dev/sdb4分区类型为linux,大小为10G
  
保留40G留作后用
   
上面我们对/dev/sdb已经分区了， 使用如下命令清空

[root@centos7 mnt]$ dd if=/dev/zero of=/dev/sdb bs=1 count=512 #清空分区的前512字节，分区表被清空，小心操作
   
View Code
  
3 parted使用
  
3.1 parted命令基础
  
复制代码
  
[root@centos7 mnt]$ parted &#8211;help
  
Usage: parted [OPTION]&#8230; [DEVICE [COMMAND [PARAMETERS]&#8230;]&#8230;]
  
Apply COMMANDs with PARAMETERS to DEVICE. If no COMMAND(s) are given, run in
  
interactive mode.

OPTIONs:
    
-h, &#8211;help displays this help message
    
-l, &#8211;list lists partition layout on all block devices
    
-m, &#8211;machine displays machine parseable output
    
-s, &#8211;script never prompts for user intervention
    
-v, &#8211;version displays the version
    
-a, &#8211;align=[none|cyl|min|opt] alignment for new partitions

COMMANDs:
    
align-check TYPE N check partition N for TYPE(min|opt)
          
alignment
    
help [COMMAND] print general help, or help on
          
COMMAND
    
mklabel,mktable LABEL-TYPE create a new disklabel (partitionM # 设置分区类型 详细使用man获取
          
table)
    
mkpart PART-TYPE [FS-TYPE] START END make a partition # 创建一个分区 start,end为M，详细信息使用man获取
    
name NUMBER NAME name partition NUMBER as NAME
    
print [devices|free|list,all|NUMBER] display the partition table, # 打印信息
          
available devices, free space, all found partitions, or a particular
          
partition
    
quit exit program # 退出
    
rescue START END rescue a lost partition near START # 救援一个丢失的分区
          
and END
    
rm NUMBER delete partition NUMBER # 删除一个分区
    
select DEVICE choose the device to edit # 选择一个分区去编辑
    
disk_set FLAG STATE change the FLAG on selected device # 改变选择分区的标记
    
disk_toggle [FLAG] toggle the state of FLAG on selected # 切换选择分区的标记
          
device
    
set NUMBER FLAG STATE change the FLAG on partition NUMBER # 改变指定分区号的标记
    
toggle [NUMBER [FLAG]] toggle the state of FLAG on partition # 切换指定分区号的标记
          
NUMBER
    
unit UNIT set the default unit to UNIT # 设置默认单位
    
version display the version number and # 显示版本
          
copyright information of GNU Parted

Report bugs to bug-parted@gnu.org
  
复制代码
  
3.2 parted实战
  
GPT分区
  
/dev/sdb1分区类型为Linux LVM，大小为30G
  
/dev/sdb2分区类型为swap，大小为20G
  
/dev/sdb3分区类型为Linux， 大小为10G
  
/dev/sdb4分区类型为linux,大小为10G
  
保留40G留作后用
  
[root@centos7 mnt]$ parted -s /dev/sdb mklabel gpt
  
[root@centos7 mnt]$ parted -s /dev/sdb unit GB mkpart primary 1 30 set 1 lvm on
  
[root@centos7 mnt]$ parted -s /dev/sdb unit GB mkpart primary 30 50 set 2 swap on
  
[root@centos7 mnt]$ parted -s /dev/sdb unit GB mkpart primary 50 60
  
[root@centos7 mnt]$ parted -s /dev/sdb unit GB mkpart primary 60 70
  
[root@centos7 mnt]$ parted -s /dev/sdb print
   
4 三种分区的比较
  
fdisk只能用于MBR分区，gdisk,parted可以用于GPT分区。
  
fdisk大多数运维工作人员已经习惯这个交互模式。
  
parted命令在创建删除分区使用命令比较方便，但是功能不是太完善，没有备份还原命令。
  
gdisk在分区上命令和fdisk风格一样， 使用方便，学习难度低且功能强大，推荐使用。