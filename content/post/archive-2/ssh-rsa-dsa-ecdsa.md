---
title: SSH 密钥类型 RSA, DSA, ecdsa
author: "-"
date: 2018-05-13T16:02:13+00:00
url: rsa
categories:
  - security
tags:
  - reprint
---
## SSH 密钥类型 RSA, DSA, ecdsa

- rsa
- ecdsa
- ed25519

优先选择ed25519

### RSA

1977年,三位数学家Rivest、Shamir 和 Adleman 设计了一种算法,可以实现非对称加密。这种算法用他们三个人的名字命名,叫做RSA算法。

在用 ssh-keygen 生成密钥对时,通常会面临是使用RSA还是DSA的选择: RSA or DSA, this is a question! 今天在这里分析一下:

原理与安全性

RSA 与 DSA 都是非对称加密算法。其中RSA的安全性是基于极其困难的大整数的分解 (两个素数的乘积) ；DSA 的安全性是基于整数有限域离散对数难题。基本上可以认为相同密钥长度的 RSA 算法与 DSA 算法安全性相当。

有点要注意,RSA 的安全性依赖于大数分解,但是否等同于大数分解一直未能得到理论上的证明,因为没有证明破解 RSA 就一定需要作大数分解。不过也不必太过担心,RSA 从诞生以来,经历了各种攻击,至今未被完全攻破 (依靠暴力破解,小于1024位密钥长度的 RSA 有被攻破的记录,但未从算法上被攻破) 。
  
用途:

DSA 只能用于数字签名, 而无法用于加密 (某些扩展可以支持加密)；RSA 即可作为数字签名, 也可以作为加密算法。不过作为加密使用的 RSA 有着随密钥长度增加,性能急剧下降的问题。
  
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

### ECDSA 椭圆曲线数字签名算法

ECDSA是用于数字签名, 是 ECC 与 DSA 的结合, 整个签名过程与 DSA 类似, 所不一样的是签名中采取的算法为 ECC, 最后签名出来的值也是分为 r,s。 而 ECC (全称Elliptic Curves Cryptography) 是一种椭圆曲线密码编码学。

ECDH 每次用一个固定的 DH key, 导致不能向前保密 (forward secrecy) , 所以一般都是用 ECDHE (ephemeral) 或其他版本的 ECDH 算法。ECDH 则是基于 ECC 的 DH ( Diffie-Hellman) 密钥交换算法。

ECC与RSA 相比,有以下的优点:

a. 相同密钥长度下,安全性能更高, 如160位ECC已经与1024位RSA、DSA有相同的安全强度。
b. 计算量小, 处理速度快, 在私钥的处理速度上 (解密和签名) , ECC远 比 RSA、DSA 快得多。
c. 存储空间占用小 ECC 的密钥尺寸和系统参数与 RSA、DSA 相比要小得多, 所以占用的存储空间小得多。
d. 带宽要求低使得 ECC 具有广泛得应用前景。
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

1) <http://security.stackexchange.com/questions/5096/rsa-vs-dsa-for-ssh-authentication-keys>
  
2) <http://iask.sina.com.cn/b/7132379.html>
  
3) <http://msdn.microsoft.com/zh-cn/library/ms978415.aspx>
  
<http://blog.sina.com.cn/s/blog_6f31085901015agu.html>

<https://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html>

RSA，DSA，ECDSA，EdDSA和Ed25519的区别
用过ssh的朋友都知道，ssh key的类型有很多种，比如dsa、rsa、 ecdsa、ed25519等，那这么多种类型，我们要如何选择呢？

说明#
RSA，DSA，ECDSA，EdDSA和Ed25519都用于数字签名，但只有RSA也可以用于加密。

RSA（Rivest–Shamir–Adleman）是最早的公钥密码系统之一，被广泛用于安全数据传输。它的安全性取决于整数分解，因此永远不需要安全的RNG（随机数生成器）。与DSA相比，RSA的签名验证速度更快，但生成速度较慢。

DSA（数字签名算法）是用于数字签名的联邦信息处理标准。它的安全性取决于离散的对数问题。与RSA相比，DSA的签名生成速度更快，但验证速度较慢。如果使用错误的数字生成器，可能会破坏安全性。

ECDSA（椭圆曲线数字签名算法）是DSA（数字签名算法）的椭圆曲线实现。椭圆曲线密码术能够以较小的密钥提供与RSA相对相同的安全级别。它还具有DSA对不良RNG敏感的缺点。

EdDSA（爱德华兹曲线数字签名算法）是一种使用基于扭曲爱德华兹曲线的Schnorr签名变体的数字签名方案。签名创建在EdDSA中是确定性的，其安全性是基于某些离散对数问题的难处理性，因此它比DSA和ECDSA更安全，后者要求每个签名都具有高质量的随机性。

Ed25519是EdDSA签名方案，但使用SHA-512 / 256和Curve25519；它是一条安全的椭圆形曲线，比DSA，ECDSA和EdDSA 提供更好的安全性，并且具有更好的性能（人为注意）。

其他说明

RSA密钥使用最广泛，因此似乎得到最好的支持。

ECDSA（在OpenSSH v5.7中引入）在计算上比DSA轻，但是除非您有一台处理能力非常低的机器，否则差异并不明显。

从OpenSSH 7.0开始，默认情况下SSH不再支持DSA密钥（ssh-dss）。根据SSH标准（RFC 4251及更高版本），DSA密钥可用于任何地方。

Ed25519在openSSH 6.5中引入。

相关文章

OpenSSH supports several signing algorithms (for authentication keys) which can be divided in two groups depending on the mathematical properties they exploit:

DSA and RSA, which rely on the practical difficulty of factoring the product of two large prime numbers,
ECDSA and Ed25519, which rely on the elliptic curve discrete logarithm problem. (example)
Elliptic curve cryptography (ECC) algorithms are a more recent addition to public key cryptosystems. One of their main advantages is their ability to provide the same level of security with smaller keys, which makes for less computationally intensive operations (i.e. faster key creation, encryption and decryption) and reduced storage and transmission requirements.

OpenSSH 7.0 deprecated and disabled support for DSA keys due to discovered vulnerabilities, therefore the choice of cryptosystem lies within RSA or one of the two types of ECC.

RSA keys will give you the greatest portability, while #Ed25519 will give you the best security but requires recent versions of client & server[2]. #ECDSA is likely more compatible than Ed25519 (though still less than RSA), but suspicions exist about its security (see below).
结论#
ssh key的类型有四种，分别是dsa、rsa、 ecdsa、ed25519。

根据数学特性，这四种类型又可以分为两大类，dsa/rsa是一类，ecdsa/ed25519是一类，后者算法更先进。

dsa因为安全问题，已不再使用了。

ecdsa因为政治原因和技术原因，也不推荐使用。

rsa是目前兼容性最好的，应用最广泛的key类型，在用ssh-keygen工具生成key的时候，默认使用的也是这种类型。不过在生成key时，如果指定的key size太小的话，也是有安全问题的，推荐key size是3072或更大。

ed25519是目前最安全、加解密速度最快的key类型，由于其数学特性，它的key的长度比rsa小很多，优先推荐使用。它目前唯一的问题就是兼容性，即在旧版本的ssh工具集中可能无法使用。不过据我目前测试，还没有发现此类问题。

总结#
    优先选择ed25519，否则选择rsa

><https://www.cnblogs.com/librarookie/p/15389876.html>
