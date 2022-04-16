---
title: yubikey
author: "-"
date: 2018-06-20T13:55:29+00:00
url: /?p=12337
categories:
  - security

tags:
  - reprint

---
## yubikey

YubiKey 4 可以同时工作在三种模式:

- OTP mode: 作为键盘设备 (HID) :
  
Yubico OTP,
  
第一次使用前需要把 KEY_ID,AES_KEY,SECRET 提交至验证服务器 (Yubico提供或者自己搭建) ,之后应用程序每次通过服务器验证密码的可靠性 (解码后SECRET对应、COUNT增大 (防止重放攻击) ) 。

- Challenge-Response: 即可以通过 HID 接口给定一个输入, 输入 HMAC 的计算结果。输入需要本地代码实现。
  
静态密码,
  
HOTP:算法与Challenge-Response类似,然而使用累加计数器代替了输入,并且HTOP是一个标准协议,许多网站和设备都兼容该标准。
  
在YubiKey中包含两个configuration slot,每一个slot可以单独配置以上模式中的其中一种,通过短触和长触来选择输入。

- U2F mode:
  
U2F是一个开源的认证标准协议,使用非对称加密算法,在每次需要认证是设备可以对challenge信息使用私钥进行签名来完成认证。作为一个开源的标准协议,Google、Dropbox等网站都支持这种协议的两步验证,然而现阶段浏览器端仅有Chrome支持。

- CCID mode, Smartcard 模式:
  
CCID (SmartCard)
   
OpenPGP card 和 PIV card, 可以用来安全地保存 RSA 私钥
  
YubiKey还可以作为标准的 OpenPGP Smart Card 使用, 用来存储 PGP 私钥 (设备中私钥是可写不可读的, 解密/签名操作在设备上完成) 。关于PGP Smart Card 的更多信息,可以参考这篇文章。

以上提到的三个功能是可以同时使用的,相互之间并不冲突。

https://wiki.archlinux.org/index.php/yubikey#Introduction
  
https://www.bookstack.cn/read/yubikey-handbook-chinese/ssh-authenticating-ssh-with-piv-and-pkcs11-client-troubleshooting.md
  
https://blog.dwx.io/yubikey4/
  
https://www.bookstack.cn/read/yubikey-handbook-chinese/piv-use-cases.md

https://bigeagle.me/2012/05/yubikey/
  
https://bigeagle.me/2016/02/yubikey-4/
  
https://blog.blahgeek.com/yubikey-intro/
>https://bitbili.net/yubikey_5_nfc_functions.html



### piv ssh key

```bash
yubico-piv-tool -s 9a -a generate -k --pin-policy=once --touch-policy=never --algorithm=ECCP256 -o public.pem
yubico-piv-tool -a verify-pin -a selfsign-certificate -s 9a -S '/CN=wiloon/' --valid-days=3650 -i public.pem -o cert.pem
yubico-piv-tool -k -a import-certificate -s 9a -i cert.pem
ssh-keygen -D /usr/lib/libykcs11.so -e
yubico-piv-tool -a status
ssh-add -s /usr/lib/libykcs11.so
ssh-add -L

Host github.com
 PKCS11Provider /usr/lib/libykcs11.so
 Port 22
 User foobar

yubico-piv-tool -s 9a  -a import-key -k --pin-policy=once --touch-policy=always -i id_rsa.pem
ssh-keygen -D /usr/lib/libykcs11.so -e
ssh-add -s /usr/lib/libykcs11.so
yubico-piv-tool -a status
```


>https://ruimarinho.gitbooks.io/yubikey-handbook/content/ssh/authenticating-ssh-with-piv-and-pkcs11-client/
>https://mdrights.github.io/os-observe/posts/2020/12/yubikey-ssh-login.html



Step 7: So far, so good. The problem comes when you unplug the device and reinsert it. SSH just gives an error "agent refused operation":

ssh babyspice.example.com
sign_and_send_pubkey: signing failed for RSA "Public key for PIV Authentication" from agent: agent refused operation
jes@babyspice.example.com's password:
It took me a little while to find out what was going on here because it wasn't mentioned in the YubiCo tutorial. Eventually I found this GitHub issue. The problem is that the SSH agent does not reinitialise libykcs11 when the YubiKey is plugged in (because it has no way to know that it should), which means libykcs11 doesn't get a chance to ask you for the PIN, which means it can't unlock the YubiKey, which means it can't use it for SSH authentication.

This seems like a pretty big oversight, but fortunately it's quite easy to work around. All you need to do is remove and re-add the keys provided by libykcs11. I added this to my ~/.bashrc based on this comment on the GitHub issue:

alias yf="ssh-add -e /usr/lib/x86_64-linux-gnu/libykcs11.so; ssh-add -s /usr/lib/x86_64-linux-gnu/libykcs11.so"


>https://incoherency.co.uk/blog/stories/yubikey.html



https://ruimarinho.gitbooks.io/yubikey-handbook/content/ssh/authenticating-ssh-with-piv-and-pkcs11-client/


## 其它

### 硬件密钥

yubikey, Nitrokey，Google Titan， CanoKeys

### 软件密钥

Solokeys，U2F-zero

## TOTP

- Google Authenticator
- Microsoft Authenticator
- Authy
- andOTP

## WebAuthn

<https://webauthn.io/>

## CanoKey

<https://blog.cubercsl.site/post/canokey-unboxing/>

CanoKey由清华大学的一些老师/学生（同时也是开源社区的大佬）所写，有软硬件（包括PCB设计）皆开源的stm32版本，也有使用密码学芯片的发售版本（其核心功能一致，只是速度较大差别），可供国内广大用户、企业选用，满足其硬件密钥乃至安全性需求。

这是「合法」的（参考《密码法》），「廉价」的（比市场同类商品价格低，功能更加丰富），「易用」的（相关软件已经发布）。

同时，用户可以体验虚拟硬件密钥，进行构建/购买前的测试与游玩！同时也欢迎用户参与核心代码库的贡献，您的贡献可能出现在下一版的发售中！

## fido2

