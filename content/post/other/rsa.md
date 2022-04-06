---
title: RSA
author: "-"
date: 2011-07-28T04:58:12+00:00
url: rsa
categories:
  - Emacs
tags:
  - reprint
---
## RSA

Java cipher

What is Java Cipher?
在计算机系统中，Java Cryptography Architecture (JCA) 是一个使用 Java 编程语言处理加解密相关操作的框架。它是 Java 安全 API 的一部分，最早是在 JDK1.1 版本的java.security包中引入的。JCA 基于”provider“架构，并且包含一系列不同作用的 API，比如加密、秘钥生成与管理、安全随机数生成、证书验证等等。这些 API 为开发人员提供了在应用代码中集成安全操作的简易方式。

Java Cryptography Extension (JCE) 是 Java 平台的一个官方标准扩展，也是 JCA 体系的一部分。JCE 为加密、密码生成和管理、消息认证码等操作提供了一个框架和具体实现。其实 Java 平台本身就包含摘要生成、数字签名等操作的接口和具体实现，JCE 提供了一个更丰富的补充。而javax.crypto.Cipher 类则是 JCE 扩展的核心。

Cipher 实例化
我们可以通过调用静态getInstance方法，传入具体的转换模式名称，就可以实例化一个 Cipher 对象。下面是实例化 Cipher 的示例代码: 

public class Encryptor {
    public byte[] encryptMessage(byte[] message, byte[] keyBytes) 
  throws InvalidKeyException, NoSuchPaddingException, NoSuchAlgorithmException {
    Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
    //...
    }
}
转换模式 (transformation) 的具体含义
转换模式 (transformation) 是 Cipher 实例化的一个核心参数。transformation 参数的格式是: 算法/工作模式/填充模式(algorithm/mode/padding)，如上述示例中AES/ECB/PKCS5Padding。

算法(Algorithm)
算法指的就是具体使用到的加解密算法的名称，且必须为英文字符串，如”AES”, “RSA”, “SHA-256” 等。

工作模式(Mode)
工作模式主要是指分组密码工作模式。分组密码工作模式允许使用同一组分组密码秘钥对于多于一块的数据进行加密，并保证其安全性。简单说就是将需要加密的原始信息分成固定长度的数据块，然后用分组密码对这些数据块进行加密。使用分组加密一般有如下场景: 

当需要加密的明文长度比较大，比如文件内容，由于硬件或者性能原因所以需要分组加密；
多次使用相同的密钥对多个分组加密，会引发一些安全问题；
分组密码工作模式本质上是一项增强密码算法或者使算法适应具体应用的技术，例如将分组密码应用于数据块组成的序列或者数据流。目前主要包括下面五种由NIST定义的工作模式: 

模式    名称    描述    典型应用
电子密码本(ECB)    Electronic CodeBook    用相同的密钥分别对明文分组独立加密    单个数据的安全传输(例如一个加密密钥)
密码分组链接(CBC)    Cipher Block Chaining    加密算法的输入是上一个密文组合下一个明文组的异或    面向分组的通用传输或者认证
密文反馈(CFB)    Cipher FeedBack    一次处理s位，上一块密文作为加密算法的输入，产生的伪随机数输出与明文异或作为下一单元的密文    面向分组的通用传输或者认证
输出反馈(OFB)    Output FeedBack    与CFB类似，只是加密算法的输入是上一次加密的输出，并且使用整个分组    噪声信道上的数据流的传输(如卫星通信)
计数器(CTR)    Counter    每个明文分组都与一个经过加密的计数器相异或。对每个后续分组计数器递增    面向分组的通用传输或者用于高速需求
填充模式(Padding)
分组密码工作模式只能加密长度等于密码分组长度的单块数据，所以通常来讲，最后一块数据也需要使用合适填充方式将数据扩展到匹配密码块大小的长度。所以填充是指在加密之前，在原始信息的开头、结尾或者中间添加特定格式的数据，使被加密信息满足固定加密长度的操作。例如我们约定块的长度为128，但是需要加密的原文长度为129，那么需要分成两个加密块，第二个加密块需要填充127长度的数据，填充模式决定怎么填充数据。

对数据在加密时进行填充、解密时去除填充则是通信双方需要重点考虑的因素。对原文进行填充，主要基于以下原因: 

首先，考虑安全性。由于对原始数据进行了填充，使原文能够“伪装”在填充后的数据中，使得攻击者很难找到真正的原文位置。
其次，由于块加密算法要求原文数据长度为固定块大小的整数倍，如果加密原文不满足这个条件，则需要在加密前填充原文数据至固定块大小的整数倍。
另外，填充也为发送方与接收方提供了一种标准的形式以约束加密原文的大小。只有加解密双方知道填充方式，才可知道如何准确移去填充的数据并进行解密。
常用的填充方式至少有5种，不同编程语言实现加解密时用到的填充多数来自于这些方式或它们的变种方式


>https://bigzuo.github.io/2019/03/27/java-cipher-tutorial/
