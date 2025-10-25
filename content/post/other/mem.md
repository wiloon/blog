---
title: linux 内存
author: lcf
date: 2012-09-25T05:30:38+00:00
url: /?p=4259
categories:
  - Linux
tags:
  - reprint
---
## linux 内存

## linux 查看内存

```bash
top
free -h
# 内存的更具体的使用情况
cat /proc/meminfo

dmidecode -t memory

dmidecode |grep -A16 "Memory Device$"

```

## 进程内存占用

```bash
top
ps aux | grep containerd
  
ps -o pid,user,%mem,rss,vsz,comm -C containerd
  
pmap PID

#ps
  
ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid' 其中rsz是是实际内存
ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid' | grep oracle | sort -nrk5

其中rsz为实际内存，上例实现按内存排序，由大到小
sudo pacman -S htop  # Arch Linux
htop

# 实时查看 containerd 服务的资源占用
systemd-cgtop

# 只看 containerd 相关的
systemd-cgtop | grep containerd
yay -S smem
sudo smem -t -k -c "pid user command rss pss uss" | grep containerd
```

### 内存映射

```bash
    cat /proc/PID/maps
    cat /proc/PID/smaps
```

### free> total 跟物理内存不一致

系统启动时会初始化相关设备，该过程会占用内存，内核启动时，也会占用一部分的内存。

[http://www.cnblogs.com/gaojun/p/3406096.html](http://www.cnblogs.com/gaojun/p/3406096.html)
