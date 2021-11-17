---
title: debian 6 (squeeze) 源列表
author: "-"
date: 2011-11-26T10:00:24+00:00
url: /?p=1644
bot_views:
  - 4
views:
  - 7
categories:
  - Linux

---
## debian 6 (squeeze) 源列表
# 这个台湾的源速度一直就很不错
  
deb http://debian.nctu.edu.tw/debian/ squeeze main non-free contrib
  
deb http://debian.nctu.edu.tw/debian/ squeeze-proposed-updates main non-free contrib


# 这个ftp的源速度很快（将http改为ftp也可) 
  
deb http://ftp.debian.org/debian/ squeeze main non-free contrib
  
deb http://ftp.debian.org/debian/ squeeze-proposed-updates main non-free contrib

#deb http://ftp.us.debian.org/debian/ squeeze main non-free contrib
  
#deb http://ftp.us.debian.org/debian/ squeeze-proposed-updates main non-free contrib

# 官方安全更新的源
  
deb http://security.debian.org/ squeeze/updates main

# 这个多媒体的源需要提前准备好额外的公钥，方法是: 
  
# 先下载公钥 debian-multimedia-keyring ，再取得root权限，
  
# 最后安装该公钥文件"dpkg -i debian-multimedia-keyring_2010.12.26_all.deb"（版本号可能会不断更新) 
  
# 更详细的请参考它的官网页面一开头的说明，地址: http://www.debian-multimedia.org/
  
deb http://ftp.debian-multimedia.org/ squeeze main non-free

# 另一个台湾的源
  
#deb http://ftp.tw.debian.org/debian/ squeeze main non-free contrib
  
#deb http://ftp.tw.debian.org/debian/ squeeze-proposed-updates main non-free contrib
  
#deb http://ftp.tw.debian.org/debian-multimedia/ squeeze main non-free

# 上海交大的源
  
#deb http://ftp.sjtu.edu.cn/debian/ squeeze main non-free contrib
  
#deb http://ftp.sjtu.edu.cn/debian/ squeeze-proposed-updates main non-free contrib
  
#deb http://ftp.sjtu.edu.cn/debian-security/ squeeze/updates main non-free contrib

# 163的源
  
#deb http://mirrors.163.com/debian/ squeeze main non-free contrib
  
#deb http://mirrors.163.com/debian/ squeeze-proposed-updates main non-free contrib
  
#deb http://mirrors.163.com/debian-security/ squeeze/updates main non-free contrib