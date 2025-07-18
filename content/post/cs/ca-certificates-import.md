---
title: ca-certificates 导入CA证书
author: "-"
date: 2025-06-24 09:18:49
url: ca
categories:
  - Security
tags:
  - reprint
  - remix
---
## ca-certificates 导入 CA 证书

## macos 导入自签名证书

在 Spotlight 里搜索 “钥匙串访问” 或者 Keychain Access, 在左侧栏里选择 System, 点击菜单栏 File> import items, 导入 自签名的 ca 证书
然后在 系统证书里面找名字是 *.wiloon.com 的证书, 双击打开, 展开 trust, when using this certificate: always trust

## archlinux ca-certificates update, 导入证书/安装证书

[https://www.archlinux.org/news/ca-certificates-update/](https://www.archlinux.org/news/ca-certificates-update/)

```bash
# .pem rename to .crt
# xxx.crt should export from sub ca
sudo cp certs/ca-cert.pem /etc/ca-certificates/trust-source/anchors/wangyue-ca.crt
sudo trust extract-compat

# 验证是否安装成功
trust list|grep wiloon.com -A 5 -B 5

openssl s_client -connect hello.wiloon.com:443

```

## chrome

Chrome（Linux/macOS）直接使用操作系统的证书信任链
关闭所有 Chrome 进程，然后再打开它以生效。

## centos

```bash
yum install -y ca-certificates
update-ca-trust force-enable
cp /tmp/$1.der /etc/pki/ca-trust/source/anchors/
update-ca-trust extract
```

## ubuntu import CA

```bash
cp foo.crt /usr/share/ca-certificates/
sudo dpkg-reconfigure ca-certificates
```

---

英文版出处: [http://majic.rs/blog/system-wide-installation-of-certificates](http://majic.rs/blog/system-wide-installation-of-certificates)
  
[https://blog.csdn.net/ziyouwayj/article/details/36371747](https://blog.csdn.net/ziyouwayj/article/details/36371747)
  
因为众所周知的原因，同步android源码成了非常痛苦的事情。迫不得已采用了goagent，但是在同步时发生经常发生SSL错误，意思是CA认证失败。网上找了一圈资料，最后明白根本的原因是系统中没有安装goagent的CA证书。这里的系统不是指firefox，也不是Chrouium。于是找到了上面这篇文章。来个对照翻译吧，水平有限，错误或生硬的地方请留言，我更正。

A lot of tutorials and how-to guides can be found on the Internet regarding the creation of self-signed certificates, or even of your own certificate authority. While the tutorials are usually very good and pretty straightforward, for some reason they seem to leave out the instructions for actually deploying the CA certificates.
  
您可以在互联网上找到许多的教程和操作指南，教您如何创建自签名证书，甚至创建你自己的证书颁发机构。这些教程非常简单易懂，但是不知出于什么原因，它们都没有说明如何在真实系统上实际部署CA证书。

Although not all applications under GNU/Linux distributions respect this, the applications very often utilise the certificates located within the /etc/ssl/certs directory. The certificates themselves are usually installed through the ca-certificates package. In order to install the custom CA certificate and integrate it properly into the system so that most applications will be able to find it, several steps should be performed.

虽然不是所有的GNU/ Linux发行版都遵循这一点，但通常linux发行版都从/ etc / ssl下/ certs目录中读取证书。系统自带的证书通常是通过ca-certificates软件包安装的。为了安装自定义的CA证书，并妥善整合到系统中，让大多数应用程序能够找到它，您需要执行以下几个步骤:

1. Make sure you have installed the ca-certificates package.

1.确认您的linux系统已经安装了ca-certificates软件包

Under Debian the package can be installed by issuing the following command:

类Debain系统(凡是使用apt包管理系统的发行版，如Ubuntu、linuxmint等)可以采用如下命令安装:

$ apt-get install ca-certificates

Under Gentoo the package can be installed by issuing the following command:

Gentoo系统可以采用如下命令安装:

$ emerge -v ca-certificates

Under Fedora the package can be installed by issuing the following command:

Fedora系统可以采用如下命令安装:

$ yum install ca-certificates

Make sure you have certificates in PEM format, with the .crt extension. For the purpose of this example the certificate file will be named Example Root.ca
  
确认您要安装的证书文件是 PEM 格式，后缀名是 .crt。例如 Root.ca

Create a subdirectory within the /usr/share/ca-certificates/ directory. For the purpose of this example the directory will be named example.com. Place the certificate authority certificate into this subdirectory.
  
3.建议在 /usr/share/ca-certificates/ 目录下创建单独的目录来保存您的CA证书文件。例如/usr/share/ca-certificates/example.com/Example Root.ca

Append a new line listing the relative path (to the /usr/share/ca-certificates/ directory) to the certificate you just copied to the file /etc/ca-certificates.conf. For the purpose of this example the line will be:
  
4.在 /etc/ca-certificates.conf 文件中添加一行: 您的证书文件去除 /usr/share/ca-certificates/ 目录后的相对路径。例如针对上面的例子，就只需要添加
  
example.com/Example Root.ca

Finally, run the update-ca-certificates command as root in order to have it regenerate the /etc/ssl/certs directory to reflect the new changes.
  
5.最后，用root权限运行update-ca-certificates 命令，它会重新收集证书并更新 /etc/ssl/certs/ca-certificates.crt文件

After these steps many utilities (like wget, for example) will be able to properly utilise the newly-installed certificate. Keep in mind that some applications do not use the certificates located withing the /etc/ssl/certs/ directory (like Firefox, or Thunderbird), and in these cases you'll have to import the certificate manually into each one of them.
  
至此，绝大多数程序就能访问您的新证书了。少数程序如Firefox、Thunderbird等不读取/etc/ssl/certs目录下的证书，则需要您在相关程序中去单独导入。
  
————————————————
  
版权声明: 本文为CSDN博主「ziyouwaYJ」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: [https://blog.csdn.net/ziyouwayj/article/details/36371747](https://blog.csdn.net/ziyouwayj/article/details/36371747)
