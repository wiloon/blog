---
title: linux samba
author: wiloon
type: post
date: 2012-02-13T11:45:25+00:00
url: /?p=2304
categories:
  - Linux

---
<pre><code class="language-bash line-numbers">#安装samba
sudo pacman -S --noconfirm samba

#创建共享目录
mkdir /home/user0

</code></pre>

### 创建Samba配置文件

<pre><code class="line-numbers">[global]
workgroup = WORKGROUP
security = user

# share0: the share folder display name
[share0]
path = /home/user0
valid users = user0
public = no
writable = yes
printable = no
create mask = 0644
</code></pre>

<pre><code class="language-bash line-numbers"># 创建用户，使用已有用户的话，可以跳过
sudo pdbedit -a user0
# set password for user，设置密码，使用系统现有的用户时，也要设置密码，samba可以跟linux系统共享用户名，但是密码是独立的。
smbpasswd -a user0
# list user
pdbedit -L -v
systemctl start smb
systemctl enable smb
</code></pre>

### 客户端

file share url: &#92;hostname0\share0

<pre><code class="language-bash line-numbers">mount -t cifs //SERVER/sharename /mnt/mountpoint -o username=username,password=password,iocharset=utf8,vers=3.1.1
</code></pre>