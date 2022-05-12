---
title: deb
author: "-"
date: 2012-01-08T04:08:51+00:00
url: deb
categories:
  - Linux
tags:
  - reprint
---
## deb
## 安装deb文件
dpkg -i filename.deb


## deb卸载
打开新立得软件包管理器

sudo synaptic

在左侧的选择框中选择Installed(local or obsolete, 再在右侧的选择框中查找需要卸载的deb包, 如果知道deb包名，直接点击 ［搜索］输入包名

选择要删的包,右击,选择［标记以便删除］

The difference between "Mark for Removal" and "Mark for Complete Removal" in Synaptic Package Manager:


**Mark for removal** removes the package, but not the configuration files associated with the package. It is equivalent to

    apt-get remove package_name 

**Mark for Complete Removal** purges the package, i.e. removes both the package files and its configuration. It is equivalent to

    apt-get --purge remove package_name 

From the Synaptic Package Manager manual:

选择完后，单击［应用］
