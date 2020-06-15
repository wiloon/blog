---
title: debian postfix dovecot
author: wiloon
type: post
date: 2013-05-12T03:36:01+00:00
url: /?p=5455
categories:
  - Web

---
<span style="color: #000000; font-size: 13px; line-height: 19px;">install postfix</span>

[shell]
  
sudo apt-get install postfix
  
[/shell]

internet site, wiloon.com;

<span style="color: #000000;">sudo dpkg-reconfigure postfix</span>

<span style="color: #000000;">4、编辑main.cf </span>

[shell]
  
emacs  /etc/postfix/main.cf

[/shel]

添加以下两行

home_mailbox = maildir/

这个步骤其实为可选操作。mailbox类型可以是mbox或者是maildir，互有优缺点。但如果将来还打算扩展webmail这类应用，最好选为Maildir，这样兼容性更好一些。对于dovecot pop3而言，倒是无所谓了。具体mbox和maildir有什么区别，去参考《postfix权威指南》

mailbox_command =

mydestination = wiloon.com,localhost.localdomain,localhost
  
mydestination

mydestination参数指定postfix接收邮件时收件人的域名，换句话说，也就是你的postfix系统要接收什么样的邮件。比如：你的用户的邮件地址为user@domain.com, 也就是你的域为domain.com, 则你就需要接收所有收件人为user_name@domain.com的邮件。与myorigin一样，缺省地，postfix使用本地主机名作为 mydestination。如：

安装mailutils

# apt-get install mailutils

创建用户user1

[shell]
  
sudo useradd -m -s /bin/bash user1
  
sudo passwd user1
  
[/shell]

<span style="color: #000000;">在mydestination后加上wiloon.com，成为这个样子： </span>

myhostname

myhostname 参数指定运行postfix邮件系统的主机的主机名。缺省地，该值被设定为本地机器名。你也可以指定该值，需要注意的是，要指定完整的主机名。如：

myhostname = mail.wiloon.com

用下面的命令测试,其实就是测试25端口是否打开

<pre>telnet localhost 25
Postfix将在终端中显示如下提示，这样你就可以用来键入SMTP命令.
Trying 127.0.0.1...
Connected to mail.fossedu.org.
Escape character is '^]'.
220 localhost.localdomain ESMTP Postfix (Ubuntu)
用下面的命令测试postfix

ehlo localhost
mail from: root@localhost
rcpt to:user1@localhost
data
Subject: My first mail on Postfix
Hi, Are you there? regards, Admin
. (Type the .[dot] in a new Line and press Enter )

quit 检查刚才创建的<code>fmaster</code>用户的收件箱

su - user1</pre>

<pre>cd /home/user1/Maildir/new</pre>

<pre>### try to send email from gmail to user1@wiloon.com</pre>



dovecot

安装POP3和IMAP支持

sudo apt-get install dovecot-imapd dovecot-pop3d<span style="color: #000000; font-size: 13px; line-height: 19px;">
 </span>

### dovecot配置

`vi /etc/dovecot/dovecot.conf`

<pre># uncomment on this line:
protocols = imap pop3
listen = *</pre>

### 配置认证方式

`vi /etc/dovecot/conf.d/10-auth.conf`

<pre># change on these line:
disable_plaintext_auth = no
auth_mechanisms = plain login</pre>

### 设置邮箱文件夹

`vi /etc/dovecot/conf.d/10-mail.conf`

<pre>mail_location = maildir:~/Maildir</pre>

### 配置认证

`vi /etc/dovecot/conf.d/10-master.conf`

<pre># commented on these line:
#unix_listener auth-userdb {
    #mode = 0600
    #user =
    #group =
  #}

# change or setup on these line:
# Postfix smtp-auth
  unix_listener /var/spool/postfix/private/auth {
    mode = 0666
    user = postfix
    group = postfix
  }</pre>

### 配置pop3

`vi /etc/dovecot/conf.d/20-pop3.conf`

<pre># uncomment on these line:
pop3_uidl_format = %08Xu%08Xv
pop3_client_workarounds = outlook-no-nuls oe-ns-eoh</pre>

### 重启dovecot

`/etc/init.d/dovecot restart`



大功告成！

使用telnet检测110(POP3)和143(IMAP)端口


  <ol title="Double click to hide line number.">
    <li>
      telnet 127.0.0.1 110
    </li>
    <li>
      Trying 127.0.0.1&#8230;
    </li>
    <li>
      Connected to mail.centos.bz (127.0.0.1).
    </li>
    <li>
      Escape character is &#8216;^]&#8217;.
    </li>
    <li>
      +OK Dovecot ready.
    </li>
    <li>
      quit
    </li>
    <li>
      +OK Logging out
    </li>
    <li>
      Connection closed by foreign host.
    </li>
    <li>
    </li>
    <li>
      telnet 127.0.0.1 143
    </li>
    <li>
      Trying 127.0.0.1&#8230;
    </li>
    <li>
      Connected to mail.centos.bz (127.0.0.1).
    </li>
    <li>
      Escape character is &#8216;^]&#8217;.
    </li>
    <li>
      * OK Dovecot ready.
    </li>
  </ol>
  
  
    9、给postfix加上如下配置
  
  
  <pre>smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination, permit
broken_sasl_auth_clients = yes</pre>
  
  
    ################&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
  


<span style="color: #000000;">#默认情况下，dovecot是不允许plaintext类型的认证的，打开 </span>

<span style="color: #000000;">&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; </span>
  
<span style="color: #000000;">重启postfix和dovecot。至此，postfix可以收信，并且foxmail可以pop3取信。测试。 </span>
  
<span style="color: #000000;">到现在foxmail还不能连接到postfix发信，原因是postfix不进行open relay，OR可不能打开，太危险了。 </span>
  
<span style="color: #000000;">两种解决方案： </span>
  
<span style="color: #000000;">a、在mail.cf里的mynetworks字段加上foxmail所在的网段。默认情况下mynetworks字段只有127.0.0.0/8，所以你telnet mail.example.com 25 后，是可以发信的。如果你确定foxmail所在的网段，加上即可。 </span>
  
<span style="color: #000000;">b、很多情况下发信客户ip是不能确定的，所以打开sasl认证。 </span>
  
<span style="color: #000000;">接下来配置sasl认证 </span>
  
<span style="color: #000000;">&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; </span>

<span style="color: #000000;">8、编辑dovecot.conf </span>
  
<span style="color: #000000;">在mechanisms字段加上login，成为这个样子： </span>

<span style="color: #000000;">mechanisms = plain login </span>

<span style="color: #000000;">编辑socket listen字段，成为这个样子： </span>

<span style="color: #000000;">引用: </span>
  
<span style="color: #000000;">socket listen { </span>
  
<span style="color: #000000;">client { </span>
  
<span style="color: #000000;">path = /var/spool/postfix/private/auth-client </span>
  
<span style="color: #000000;">mode = 0660 </span>
  
<span style="color: #000000;">user = postfix </span>
  
<span style="color: #000000;">group = postfix </span>
  
<span style="color: #000000;">} </span>
  
<span style="color: #000000;">} </span>

<span style="color: #000000;">9、给postfix加上如下配置 </span>

<pre>smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination, permit
broken_sasl_auth_clients = yes</pre>

<span style="color: #000000;">10、重起postfix（sudo service postfix restart）和dovecot（sudo service dovecot restart）。不出意外的话，已经可以通过foxmail正常收发邮件了 </span>

<span style="color: #000000;">注： </span>
  
<span style="color: #000000;">1、这样的配置对认证过程不加密，如果害怕密码被监听，就进一步加上ssl好了。 </span>
  
<span style="color: #000000;">2、如果被hotmail等退信的话。大部分情况下有两种可能：a、没有PTR记录，找你的ISP做。b、你的IP属于垃圾邮件监控地址(俗称上榜，呵呵)，去查查看。比如www.spamhaus.org(hotmail就是用这个的)，如果属于pbl，申请取消就好了，如果sbl这些，那就只能找你的ISP解决了。gmail则比较奇怪。如果gmail退信的话，试着改一下mail.cf中mydestination的顺序，把localhost改到前面。改成这个样子： </span>
  
<span style="color: #000000;">“mydestination = localhost, localhost.example.com, mail.example.com, example.com” </span>
  
<span style="color: #000000;">很多人就这样把问题解决了，但似乎谁都不知道原理 🙂</span>

<http://goahead2010.iteye.com/blog/1911165>

<https://help.ubuntu.com/community/PostfixBasicSetupHowto>

<http://yubosun.akcms.com/tech/postfix-dovecot-smtp.htm>

<http://forum.ubuntu.org.cn/viewtopic.php?f=54&t=170026>

<http://myworkrecord.blog.51cto.com/3407230/649209>

