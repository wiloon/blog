---
title: ssh agent forward
author: wiloon
type: post
date: 2020-04-21T17:24:23+00:00
url: /?p=16034
categories:
  - Uncategorized

---
https://www.jianshu.com/p/12de50582e63

ssh到node1
  
由node1跳板到任意机器。
  
然而失败了。

XiaoleideMacBook-Pro:~ professor$ vi .bashrc
  
alias go-node1='ssh -p 1046 hzlixiaolei@10.165.xxx.xxx'
  
XiaoleideMacBook-Pro:~ professor$ go-node1
  
-bash: go-node1: command not found
  
XiaoleideMacBook-Pro:~ professor$ source .bashrc
  
-bash: SSH\_AUTH\_SOCK=/var/folders/9x/7zl7w59n55s3wb_wjg7d5zfh0000gn/T//ssh-XpUY3kpYkJnP/agent.9483;: No such file or directory
  
XiaoleideMacBook-Pro:~ professor$ go-node1

The programs included with the Debian GNU/Linux system are free software;
  
the exact distribution terms for each program are described in the
  
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
  
permitted by applicable law.
  
Last login: Mon Feb 6 15:51:21 2017 from 10.165.xx.xx
  
hzlixiaolei@node1:~$go-node2
  
(public key denied)
  
如图所示，我从node1往node2跳的时候出现公钥无效。

解决办法
  
其实这里的问题就在于我没有开ssh-agent.

正确配置ssh-agent forwardi配置即可成功：

1，配置本地ssh-agent forwarding，及测试结果
  
ForwardAgent yes
  
打开本地ssh client的forwardAgent

XiaoleideMacBook-Pro:~ professor$:vi /etc/ssh/ssh_config
  
Host *
      
ForwardAgent yes
      
ForwardX11 yes
  
XiaoleideMacBook-Pro:ssh professor$ echo "$SSH\_AUTH\_SOCK"
  
/private/tmp/com.apple.launchd.xkodPCHoTj/Listeners
  
2， 配置云主机的SSH-agent forwarding
  
配置步骤同上

3，查看本地SSH agent是否携带本地的ssh key
  
Mac特有的一个问题，要注意
  
On Mac OS X, ssh-agent will "forget" this key, once it gets restarted during reboots. But you can import your SSH keys into Keychain using this command:

XiaoleideMacBook-Pro:ssh professor$ ssh-add -L
  
好了，问题解决。

SSH, SSH agent & SSH agent Forwarding
  
这里，必须需要说下这三者的联系。以便于大家理论上理解。图文并茂介绍下：

1，我们常用的SSH工作原理
  
通过publickey access：
  
Step1，用户发起连接，携带者用户名

1.png
  
Step2，ssh守护进程（sshd）在Server上查看authorized_keys文件，基于publickey构造一个口令盘问发送给SSH client
  
The ssh daemon on the server looks in the user's authorized_keys file, constructs a challenge based on the public key found there, and sends this challenge back to the user's ssh client.

2.png
  
Step3，SSH client收到后，在本地茶韵privatekey（默认id_rsa文件），此时如果有密码，会要求输入密码。

3.png
  
Step4，ssh client通过privatekey构造一个响应。发送给sshd。注意：这里并不会发送privatekey本身。
  
Step5，验证，授权成功

4.png
  
2，SSH agent是干嘛的
  
如果每次我们都SSH到某个server，我们如果privatekey有密码，如果没有ssh agent，每次我们都会需要被告知要输入密码。有了ssh Agent，就不需要了。因为它负责管理key。

与上面相比，唯一的区别在第三步和第四步：

5.png
  
6.png
  
如图所示，根据privatekey构造响应的操作有ssh-agent来做了。ssh client没有和privatekey有联系。所以后面的访问，都是ssh-agent来管理，又因为我们之前输入过密码，ssh-agent仍然记录这个状态，所以之后就不用再输入密码了。
  
可谓一劳永逸。

3，ssh agent forwarding
  
简单来说，agent forwarding运行一串的ssh连接。将sshd的口令盘问直接发送到最初始的ssh client，而不需要任何中间集群的认证。
  
如果按照我们上面的配置，配置好了agent forwarding，它是如何工作的：
  
Step1，基于上面的ssh到server1，用户在server1上开始发起到server2的链接（这一步和之前一样）

7.png
  
8.png
  
Step2: server2的sshd查询用户的authorized_keys文件，并像之前一样构造一个口令盘问发回给server1的ssh。下面神奇的事情就发生了：server1的ssh发送给自己的sshd，并再一次relay给我们pc的ssh。

9.png
  
10.png
  
Step3: 后面的步骤就是PC的ssh agent根据privatekey构造key response并串行的发到server2的sshd上。然后完成鉴权。

11.png
  
12.png
  
Step4：如果需要在往Server3，4，N，仍然有效。

作者：professorLea
  
链接：https://www.jianshu.com/p/12de50582e63
  
来源：简书
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。