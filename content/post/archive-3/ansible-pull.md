---
title: ansible-pull
author: "-"
date: 2020-01-11T06:04:50+00:00
url: /?p=15315
categories:
  - Inbox
tags:
  - reprint
---
## ansible-pull
ansible-pull

该指令的使用涉及Ansible的另一种工作模式: pull模式 (Ansible默认使用push模式) 。这和通常使用的push模式工作机理刚好相反，其适用于以下场景: ①你有数量巨大的机器需要配置，即使使用高并发线程依旧要花费很多时间；②你要在刚启动的、没有网络连接的主机上运行Anisble。

ansible-pull命令使用格式如下: 
  
ansible-pull [options] [playbook.yml]
  
通过ansible-pull结合Git和crontab一并实现，其原理如下: 通过crontab定期拉取指定的Git版本到本地，并以指定模式自动运行预先制订好的指令。

具体示例参考如下: 
  
*/20 \* \* \* * root /usr/local/bin/ansible-pull -o -C 2.1.0 -d /srv/www/king-gw/ -i /etc/ansible/hosts -U git:// git.kingifa.com/king-gw-ansiblepull >> /var/log/ansible-pull.log 2>&1
  
ansible-pull通常在配置大批量机器的场景下会使用，灵活性稍有欠缺，但效率几乎可以\***提升，对运维人员的技术水平和前瞻性规划有较高要求。