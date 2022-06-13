---
title: AES
author: "-"
date: 2018-02-07T05:27:57+00:00
url: aes
categories:
  - Security
tags:
  - reprint
---
## AES

### AES算法简介

AES的全称是Advanced Encryption Standard,意思是高级加密标准。它的出现主要是为了取代DES加密算法的,因为我们都知道DES算法的密钥长度是56Bit,因此算法的理论安全强度是2的56次方。但二十世纪中后期正是计算机飞速发展的阶段,元器件制造工艺的进步使得计算机的处理能力越来越强,虽然出现了3DES的加密方法,但由于它的加密时间是DES算法的3倍多,64Bit的分组大小相对较小,所以还是不能满足人们对安全性的要求。于是1997年1月2号,美国国家标准技术研究所宣布希望征集高级加密标准,用以取代DES。AES也得到了全世界很多密码工作者的响应,先后有很多人提交了自己设计的算法。最终有5个候选算法进入最后一轮: Rijndael,Serpent,Twofish,RC6和MARS。最终经过安全性分析、软硬件性能评估等严格的步骤,Rijndael算法获胜。

在密码标准征集中,所有AES候选提交方案都必须满足以下标准:

分组大小为128位的分组密码。
必须支持三种密码标准: 128位、192位和256位。
比提交的其他算法更安全。
在软件和硬件实现上都很高效。
AES密码与分组密码Rijndael基本上完全一致, Rijndael 分组大小和密钥大小都可以为128位、192位和256位。然而AES只要求分组大小为128位,因此只有分组长度为128Bit的Rijndael才称为AES算法。本文只对分组大小128位,密钥长度也为128位的Rijndael算法进行分析。密钥长度为192位和256位的处理方式和128位的处理方式类似,只不过密钥长度每增加64位,算法的循环次数就增加2轮,128位循环10轮、192位循环12轮、256位循环14轮。

### ECB模式 (电子密码本模式: Electronic codebook)
  
ECB是最简单的块密码加密模式,加密前根据加密块大小 (如AES为128位) 分成若干块,之后将每块使用相同的密钥单独加密,解密同理。

### CBC模式 (密码分组链接: Cipher-block chaining)
  
CBC模式对于每个待加密的密码块在加密前会先与前一个密码块的密文异或然后再用加密器加密。第一个明文块与一个叫初始化向量的数据块异或。
  
CBC模式相比ECB有更高的保密性,但由于对每个数据块的加密依赖与前一个数据块的加密所以加密无法并行。与ECB一样在加密前需要对数据进行填充,不是很适合对流数据进行加密。
  
### CFB模式(密文反馈:Cipher feedback)
  
与ECB和CBC模式只能够加密块数据不同,CFB能够将块密文 (Block Cipher) 转换为流密文 (Stream Cipher) 。
  
注意:CFB、OFB和CTR模式中解密也都是用的加密器而非解密器。
  
CFB的加密工作分为两部分:

将一前段加密得到的密文再加密；
  
将第1步加密得到的数据与当前段的明文异或。
  
由于加密流程和解密流程中被块加密器加密的数据是前一段密文,因此即使明文数据的长度不是加密块大小的整数倍也是不需要填充的,这保证了数据长度在加密前后是相同的。

OFB模式 (输出反馈: Output feedback)
  
OFB是先用块加密器生成密钥流 (Keystream) ,然后再将密钥流与明文流异或得到密文流,解密是先用块加密器生成密钥流,再将密钥流与密文流异或得到明文,由于异或操作的对称性所以加密和解密的流程是完全一样的。

<http://blog.csdn.net/songdeitao/article/details/17267443>
  
<https://blog.csdn.net/qq_28205153/article/details/55798628>

```java
  
import javax.crypto.Cipher;
  
import javax.crypto.spec.SecretKeySpec;

public class AESCodec {
      
public static byte[] encrypt(String key, byte[] value) {
          
try {
              
SecretKeySpec skeySpec = new SecretKeySpec(key.getBytes("UTF-8"), "AES");
              
Cipher cipher = Cipher.getInstance("AES/ECB/Nopadding");
              
cipher.init(Cipher.ENCRYPT_MODE, skeySpec);
              
return cipher.doFinal(value);
          
} catch (Exception ex) {
              
ex.printStackTrace();
          
}
          
return null;
      
}

public static byte[] decrypt(String key, byte[] encrypted) {
          
try {
              
SecretKeySpec skeySpec = new SecretKeySpec(key.getBytes("UTF-8"), "AES");
              
Cipher cipher = Cipher.getInstance("AES/ECB/Nopadding");
              
cipher.init(Cipher.DECRYPT_MODE, skeySpec);
              
byte[] original = cipher.doFinal(encrypted);
              
return original;
          
} catch (Exception ex) {
              
ex.printStackTrace();
          
}
          
return null;
      
}

}
  
```

<https://blog.poxiao.me/p/advanced-encryption-standard-and-block-cipher-mode/>
  
<https://github.com/matt-wu/AES>
