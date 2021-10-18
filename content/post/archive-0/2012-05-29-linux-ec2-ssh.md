---
title: linux ec2 ssh
author: "-"
type: post
date: 2012-05-29T13:04:13+00:00
url: /?p=3291
categories:
  - Linux
  - Network

---
# linux ec2 ssh
将相应的pem保存到 .ssh 文件夹。在该文件内建立config文件，输入以下配置内容: 

```bash
  
Host aws
  
HostName xxx.xxx.xxx.xxx
  
User ubuntu
  
IdentityFile ~/.ssh/your-key.pem
  
CompressionLevel 6
  
DynamicForward localhost:3128
  
```

Host 为设定一个名字给该连接，可任意选，此处用aws；
  
HostName 这里输入附加到该Instance的Elastic IP， 或者 public DNS 的连接，这些都可从Dashboard instance 信息里面看到；
  
User 因为之前EC2上建立的是ubuntu AMI，其默认的登录用户名为 ubuntu；
  
IdentityFile 需输入你的 pem 文件的路径；
  
DynamicForward 默认用localhost:3128，在后面的浏览器设置中要用到。

到此ssh配置完成。从temnial输入: 

  
    
      ssh aws
    
  

即可看到从远程EC2 Instance返回的登录成功信息。

###### 通用的浏览器配置

前面是 Windows 用户和 Linux用户各自的SSH配置。接下来是通用的浏览器配置。

这里以Firefox为例。Preference -> Advanced -> Network -> Settings, 选择手动代理设置，SOCKS Host 中输入 localhost， 端口号3128 ， SOCKS vs。OK 确认。浏览器配置完毕。

###### 这里针对 Firefox 再附加一点内容: 

发现用同样的代理配置，其他浏览器正常工作，偏偏就 Firefox 不能登录 Facebook 和 Twitter，而除这两个外，其他墙外网站却都可以正常浏览。

Google了一圈，现总结如下: 

  * 在**Firefox**地址栏输入 **about:config **
  * 有安全提示，点击继续；
  * 找到"**network.proxy.socks_remote_dns**"，双击改为**True**（默认False) ；
  * 可能需要重启Firefox。

  已验证可行。
