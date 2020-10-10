+++
author = "w1100n"
date = "2020-10-09 14:34:24" 
title = "ubuntu basic"

+++

### mirror
    vim /etc/apt/sources.list
    %s/archive.ubuntu.com/mirrors.aliyun.com/g

### 开发环境
    export DISPLAY=172.18.80.1:0 # windows 里ipconfig看到的连接wsl的ip
    apt install git-svn
    apt install openjdk-8-jdk
    apt install maven
    # config ~/.m2/settings.xml
    apt install nautilus
    sudo apt-get install ttf-wqy-microhei  #文泉驿-微米黑
    sudo apt-get install ttf-wqy-zenhei  #文泉驿-正黑
    sudo apt-get install xfonts-wqy #文泉驿-点阵宋体
    sudo apt install keepassxc


### 中文乱码问题
    # 安装中文支持包language-pack-zh-hans
    sudo apt-get install language-pack-zh-hans
    # 设置语言
    vim /etc/environment
    ##中文语言环境, 设置后vim进程编辑状态屏幕下方会显示中文"插入"的那种
    LANG="zh_CN.UTF-8"
    LANGUAGE="zh_CN:zh:en_US:en"
    ## 英文环境 
    LANG="en_US.UTF-8"
    LANGUAGE="en_US:en" 

    vim /var/lib/locales/supported.d/local
    en_US.UTF-8 UTF-8
    zh_CN.UTF-8 UTF-8
    zh_CN.GBK GBK
    zh_CN GB2312

    sudo locale-gen
    # 中文乱码是空格的情况，安装中文字体解决
    sudo apt-get install fonts-droid-fallback ttf-wqy-zenhei ttf-wqy-microhei fonts-arphic-ukai fonts-arphic-uming

<https://blog.csdn.net/weixin_39792252/article/details/80415550>

### 查看软件安装位置
    dpkg -L openjdk-8-source
    whereis openjdk-8-source

### 查询版本
    apt show openjdk-8-source
    dpkg -l openjdk-8-source