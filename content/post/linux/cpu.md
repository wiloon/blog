---
title: '查CPU,  核心数'
author: "-"
date: 2011-08-07T03:50:32+00:00
url: /?p=405
categories:
  - Linux

tags:
  - reprint
---
## '查CPU,  核心数'
```bash
cat /proc/cpuinfo |grep name

# 总核数 = 物理CPU个数 X 每颗物理CPU的核数 
# 总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数

# 查看物理CPU个数
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

# 查看每个物理CPU中core的个数(即核数)
cat /proc/cpuinfo| grep "cpu cores"| uniq

# 查看逻辑CPU的个数
cat /proc/cpuinfo| grep "processor"| wc -l
grep 'model name' /proc/cpuinfo | wc -l

```