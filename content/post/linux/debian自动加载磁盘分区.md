---
title: debian自动加载磁盘分区
author: "-"
date: 2011-12-10T10:38:00+00:00
url: /?p=1831
categories:
  - Linux

tags:
  - reprint
---
## debian自动加载磁盘分区
Linux下面有个加载分区的配置文件，/etc/fstab
  
里面的分区标识是使用分区的UUID来分别的，在ubuntu下面可以使用命令: 
  
sudo blkid
  
来查看具体各个分区的UUID
  
然后在/etc/fstab文件中加上自己的加载分区的相应命令: 
  
UUID=e06ae965-4a0f-4448-8281-9b2bac150c07 /home/bing/android ext4 default 0 3
  
由于此处是挂载到/home目录的，不知道能不能成功加载，
  
上面的那个命令会出现下面的问题: 
  
Error mounting: mount exited with exit code 1: helper failed with:
  
mount: only root can mount /dev/sda8 on /home/bing/android
  
网上查了一下，所以把上面的命令改为: 
  
UUID=e06ae965-4a0f-4448-8281-9b2bac150c07 /home/bing/android ext4 auto,user,rw 0 3
  
这样好像是可以的，，，
  
记一下，防止忘记了。。。
  
最新的动态，应该使用下面命令加载系统的时候，会出现一个问题，那就是这个分区可以读写，但是不能执行程序，，
  
连root用户都没有权限执行程序，应该是指定了user这个群组了，，，
  
UUID=e06ae965-4a0f-4448-8281-9b2bac150c07 /home/bing/android ext4 auto,user,rw 0 3
  
所以办法也是行不通的，
  
后来再检查的时候才发现原先那条加载命令写错了(应该是defaults)，汗，，，，
  
换成下面的可以加载了，也可以读写执行了，，
  
UUID=e06ae965-4a0f-4448-8281-9b2bac150c07 /home/bing/android ext4 defaults 0 2
  
第一列: label
  
第二列: 挂载点
  
第三列: 分区的文件系统
  
第四列: 文件系统挂载选项,看附件啦
  
第五列: 是否被dump作用。0代表不要做dump 备份，1代表要每天进行dump的动作。 2 也代表其它不定日期的dump备份动作，通常这个数值不是0就是1啦！
  
第六列: 是否以fsck检查分区 (开机时候检查分区) 0为不检查，1为开机的时候检查，2为在稍后的时间检查
  
如果不行的话，应该可以在.bashrc文件中直接mount吧
  
sudo mount -t ext4 /dev/sda8 /home/bing/android
  
fstab文件结尾要有一个空行.....