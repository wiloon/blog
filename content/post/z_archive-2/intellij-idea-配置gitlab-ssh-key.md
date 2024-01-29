---
title: intellij idea 配置git ssh key
author: "-"
date: 2019-02-27T15:48:53+00:00
url: /?p=13731
categories:
  - Inbox
tags:
  - reprint
---
## intellij idea 配置git ssh key

把私钥放入目录 `C:\Users\user0\.ssh`, 私钥不需要转换成 ppk 格式.

[https://blog.csdn.net/u010348570/article/details/81204371](https://blog.csdn.net/u010348570/article/details/81204371)

1 安装git,登录官网[https://www.git-scm.com/download/](https://www.git-scm.com/download/) ,选择相应系统版本,下载后安装好。

公司网慢的可以用第三方的软件管家下载。

2 打开git bash,不需要进入任何目录,直接输入 ssh-keygen -t rsa -C 'xxx@xxx.com','xxx@xxx.com'为gitlab上的登录账户。一路回车。

3 打开生成的密钥文件,目录为当前系统登录者的用户目录

4 将id_rsa.pub文件里面的内容拷贝,登录公司gitlab服务器,找到ssh key配置位置Settings。有的在左侧目录处,有的则需要在自己头像的位置单击。

5 点击SSH Keys ,将上一步拷贝的内容拷贝到key下的方框中。Title可以填写一个自己的标识。

6 打开intellij idea , File -> Settings,输入git,配置下git.exe

## 7 选择 VCS -> Checkout from Version Control -> Git,将gitlab上面项目的ssh路径复制,点击Test,提示Connection successful,后面一路点击next即可

作者: 叫我放猪之人
  
来源: CSDN
  
原文: [https://blog.csdn.net/u010348570/article/details/81204371](https://blog.csdn.net/u010348570/article/details/81204371)
  
版权声明: 本文为博主原创文章,转载请附上博文链接！
