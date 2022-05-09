---
title: Inotify
author: "-"
date: 2016-12-24T11:43:10+00:00
url: /?p=9619
categories:
  - Inbox
tags:
  - reprint
---
## Inotify

sudo pacman -S inotify-tools
sudo inotifywait -rme access,modify,open /xxx/xxx

inotifywait命令参数 -m是要持续监视变化。 -r使用递归形式监视目录。 -q减少冗余信息,只打印出需要的信息。 -e指定要监视的事件列表。 -timefmt是指定时间的输出格式。 -format指定文件变化的详细信息。 可监听的事件 事件 描述 access 访问,读取文件。 modify 修改,文件内容被修改。 attrib 属性,文件元数据被修改。 move 移动,对文件进行移动操作。 create 创建,生成新文件 open 打开,对文件进行打开操作。 close 关闭,对文件进行关闭操作。 delete 删除,文件被删除。

http://man.linuxde.net/inotifywait

http://www.infoq.com/cn/articles/inotify-linux-file-system-event-monitoring
https://weizhimiao.github.io/2016/10/29/Linux%E4%B8%AD%E9%80%9A%E8%BF%87inotify-tools%E5%AE%9E%E7%8E%B0%E7%9B%91%E6%8E%A7%E6%96%87%E4%BB%B6%E5%8F%98%E5%8C%96/
