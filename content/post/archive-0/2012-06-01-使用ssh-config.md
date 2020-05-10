---
title: ssh config
author: wiloon
type: post
date: 2012-06-01T14:25:14+00:00
url: /?p=3304
categories:
  - Linux

---
### 使用通配符 (wildcard)

<pre><code class="language-bash line-numbers">vim .ssh/config

host 10.60.*
    user root

</code></pre>

SSH 参数配置有3个层次：

命令行参数，如-p 10086, -i /path/to/identity_file 等选项来设置SSH的端口号或认证证书位置
  
针对某个用户的配置文件，所在路径为~/.ssh/config，默认是不存在的，需要手动创建
  
针对系统所有用户的配置文件，，所在路径为/etc/ssh/ssh_config
  
参数重要性的顺序也是1>2>3，即越近的配置重要性越高。

用户配置文件在 ~/.ssh/config, 没有的话新建一个
  
Host 名称(自己决定，方便输入记忆的)
      
HostName 主机名
      
Port 22
      
User 登录的用户名
      
IdentityFile 证书文件路径

Host
  
Host配置项标识了一个配置区段。
  
ssh配置项参数值可以使用通配符：*代表0～n个非空白字符，?代表一个非空白字符，!表示例外通配。
  
我们可以在系统配置文件中看到一个匹配所有host的默认配置区段：

<pre><code class="language-bash line-numbers">$ cat /etc/ssh/ssh_config | grep '^Host'
</code></pre>

Host *
  
这里有一些默认配置项，我们可以在用户配置文件中覆盖这些默认配置。

<pre><code class="language-bash line-numbers">Host router
     HostName 192.168.1.1
     Port 22
     User root
     IdentityFile ~/.ssh/id_rsa
</code></pre>

使用ssh的配置文件可以在很大程度上方便各种操作，特别适应于有多个ssh帐号、使用非标准端口或者写脚本等情况。

man ssh_config
  
可以查看手册

如果之前是用密码方式来登录ssh，需要先改用证书方式。可以看最后面生成SSH证书

两个SSH帐号，一个是github的，一个是其他服务器的，证书文件正如其名，那么可以这样写

Host github.com
      
HostName github.com
      
User git
      
IdentityFile ~/.ssh/github

注意，github的Host必须写成”github.com”。你可以会有其他要求，比如指定端口号、绑定本地端口，这些都可以通过man来查询，比如

Port 端口号
  
DynamicForward 本地端口号
  
如果服务器同时有ipv4/ipv6地址，HostName使用域名会比较方便

使用

有了这些配置，很多操作就非常简化了。比如登录服务器

ssh server
  
传输文件

scp server:~/test .
  
如果使用Putty等工具，可能需要一些其他操作(转换私钥格式，貌似)，自行搜索吧

生成SSH证书

登入服务器端，生成密钥(你使用哪个用户名登录，就在哪个用户名下生成)

ssh-keygen -t rsa
  
会询问将密钥放在何处，默认即可。然后是输入密码，留空(否则你登录不仅需要私钥还要输入密码)。

完成后在~/.ssh目录下会生成另个文件id\_rsa、id\_rsa.pub，一个私钥一个公钥。接着执行

cd ~/.ssh
  
cat id\_rsa.pub >> authorized\_keys
  
chmod 600 authorized_keys
  
再将id_rsa取回本地，放入~/.ssh并将权限设为400。

服务器端，删掉这两个文件，并修改sshd配置。编辑/etc/ssh/sshd_config如下

PubkeyAuthentication yes
  
PasswordAuthentication no
  
之后重启sshd服务
  
https://vra.github.io/2017/07/09/ssh-config/
  
http://www.lainme.com/doku.php/blog/2011/01/%E4%BD%BF%E7%94%A8ssh_config