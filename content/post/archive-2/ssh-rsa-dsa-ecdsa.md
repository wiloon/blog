---
title: SSH 密钥类型 RSA, DSA, ecdsa
author: "-"
date: 2018-05-13T16:02:13+00:00
url: rsa
categories:
  - ssh

tags:
  - reprint
---
## SSH 密钥类型 RSA, DSA, ecdsa
### RSA
1977年,三位数学家Rivest、Shamir 和 Adleman 设计了一种算法,可以实现非对称加密。这种算法用他们三个人的名字命名,叫做RSA算法。

在用 ssh-keygen 生成密钥对时,通常会面临是使用RSA还是DSA的选择: RSA or DSA, this is a question! 今天在这里分析一下: 

原理与安全性

RSA 与 DSA 都是非对称加密算法。其中RSA的安全性是基于极其困难的大整数的分解 (两个素数的乘积) ；DSA 的安全性是基于整数有限域离散对数难题。基本上可以认为相同密钥长度的 RSA 算法与 DSA 算法安全性相当。

有点要注意,RSA 的安全性依赖于大数分解,但是否等同于大数分解一直未能得到理论上的证明,因为没有证明破解 RSA 就一定需要作大数分解。不过也不必太过担心,RSA 从诞生以来,经历了各种攻击,至今未被完全攻破 (依靠暴力破解,小于1024位密钥长度的 RSA 有被攻破的记录,但未从算法上被攻破) 。
  
用途: 

DSA 只能用于数字签名,而无法用于加密 (某些扩展可以支持加密) ；RSA 即可作为数字签名,也可以作为加密算法。不过作为加密使用的 RSA 有着随密钥长度增加,性能急剧下降的问题。
  
性能: 

相同密钥长度下,DSA 做签名时速度更快,但做签名验证时速度较慢,一般情况验证签名的次数多于签名的次数。

相同密钥长度下,DSA  (在扩展支持下) 解密密文更快,而加密更慢；RSA 正好反过来,一般来说解密次数多于加密次数。不过由于非对称加密算法的先天性能问题,两者都不是加密的好选择。
  
业界支持: 

在业界支持方面,RSA 显然是赢家。RSA 具有更为广泛的部署与支持。
  
使用 ssh-keygen 时的选择: 

上面说了那么多,可以看到RSA 与 DSA 各有优缺点。回到开头的问题,在使用 ssh-keygen 时,RSA 与 DSA到底选哪个？ 比较有意思的是,这个问题最终答案与上面那些优缺点无关。虽然理论上可以生成更长长度的 DSA 密钥  (NIST FIPS 186-3) ,但ssh-keygen在生成 DSA 密钥时,其长度只能为1024位 (基于NIST FIPS 186-2) ；而 ssh-keygen 在 RSA 的密钥长度上没有限制。

由于小于1024位密钥长度的 RSA 已经有被攻破的记录,所以说现在: RSA 2048 位密钥是更好的选择。
  
其它选择: 

RSA 与 DSA 各有优缺点,那有没一个更好的选择呢？答案是肯定的,ECC (Elliptic Curves Cryptography) : 椭圆曲线算法。

ECC 与 RSA 相比,有以下的优点: 
  
 (1) 相同密钥长度下,安全性能更高,如160位ECC已经与1024位RSA、DSA有相同的安全强度。
  
 (2) 计算量小,处理速度快,在私钥的处理速度上 (解密和签名) ,ECC远 比RSA、DSA快得多。
  
 (3) 存储空间占用小 ECC的密钥尺寸和系统参数与RSA、DSA相比要小得多, 所以占用的存储空间小得多。
  
 (4) 带宽要求低使得ECC具有广泛得应用前景。

在 ssh-keygen 中,ECC 算法的相应参数是 "-t ecdsa"。可惜的是由于椭圆曲线算法只有在较新版本的 openssl 与 ssh-keygen 中才被支持,而无法得到普遍使用而去完全替代 RSA/DSA。不过由于椭圆曲线算法的优点,使其取代 RSA/DSA 而成为新一代通用的非对称加密算法成为可能,至少 SET 协议的制定者们已经把它作为下一代 SET 协议中缺省的公钥密码算法了。


### ECDSA椭圆曲线数字签名算法
ECDSA是用于数字签名,是ECC与DSA的结合,整个签名过程与DSA类似,所不一样的是签名中采取的算法为ECC,最后签名出来的值也是分为r,s。而ECC (全称Elliptic Curves Cryptography) 是一种椭圆曲线密码编码学。

ECDH每次用一个固定的DH key,导致不能向前保密 (forward secrecy) ,所以一般都是用ECDHE (ephemeral) 或其他版本的ECDH算法。ECDH则是基于ECC的DH ( Diffie-Hellman) 密钥交换算法。

ECC与RSA 相比,有以下的优点: 

a. 相同密钥长度下,安全性能更高,如160位ECC已经与1024位RSA、DSA有相同的安全强度。
b. 计算量小,处理速度快,在私钥的处理速度上 (解密和签名) ,ECC远 比RSA、DSA快得多。
c. 存储空间占用小 ECC的密钥尺寸和系统参数与RSA、DSA相比要小得多, 所以占用的存储空间小得多。
d. 带宽要求低使得ECC具有广泛得应用前景。
下表是ECC和RSA安全性比较

攻破时间(MIPS年)RSA/DSA(密钥长度)ECC密钥长度RSA/ECC密钥长度比1045121065: 11087681326: 1101110241607: 11020204821010: 110782100060035: 1

下表是RSA和ECC速度比较

功能Security Builder 1.2BSAFE 3.0163位ECC(ms)1,023位RSA(ms)密钥对生成3.84,708.3签名2.1(ECNRA)228.43.0(ECDSA)认证9.9(ECNRA)12.710.7(ECDSA)Diffie—Hellman密钥交换7.31,654.0

在 ECDHE 密钥交换中,服务端使用证书私钥对相关信息进行签名,如果浏览器能用证书公钥验证签名,就说明服务端确实拥有对应私钥,从而完成了服务端认证。密钥交换和服务端认证是完全分开的。

可用于 ECDHE 数字签名的算法主要有 RSA 和 ECDSA,也就是目前密钥交换 + 签名有三种主流选择: 

RSA 密钥交换 (无需签名) ；
ECDHE 密钥交换、RSA 签名；
ECDHE 密钥交换、ECDSA 签名；



参考: 

1) http://security.stackexchange.com/questions/5096/rsa-vs-dsa-for-ssh-authentication-keys
  
2) http://iask.sina.com.cn/b/7132379.html
  
3) http://msdn.microsoft.com/zh-cn/library/ms978415.aspx
  
http://blog.sina.com.cn/s/blog_6f31085901015agu.html

https://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html

