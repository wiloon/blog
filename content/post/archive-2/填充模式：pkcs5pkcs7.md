---
title: '填充模式,PKCS#5/PKCS7'
author: "-"
date: 2018-07-10T02:48:44+00:00
url: /?p=12418
categories:
  - Inbox
tags:
  - reprint
---
## '填充模式,PKCS#5/PKCS7'
<https://blog.csdn.net/test1280/article/details/75268255>

填充模式: PKCS#5/PKCS7
  
首先我们要了解下啥是填充模式。

在分组加密算法中 (例如DES) ,我们首先要将原文进行分组,然后每个分组进行加密,然后组装密文。

其中有一步是分组。

如何分组？

假设我们现在的数据长度是24字节,BlockSize是8字节,那么很容易分成3组,一组8字节；

考虑过一个问题没,如果现有的待加密数据不是BlockSize的整数倍,那该如何分组？

例如,有一个17字节的数据,BlockSize是8字节,怎么分组？

我们可以对原文进行填充 (padding) ,将其填充到8字节的整数倍！

假设使用PKCS#5进行填充 (以下都是以PKCS#5为示例) ,BlockSize是8字节 (64bit) :

待加密数据原长度为1字节:
  
0x41
  
填充后:
  
0x410x070x070x070x070x070x070x07
  
待加密数据原长度为2字节:
  
0x410x41
  
填充后:
  
0x410x410x060x060x060x060x060x06
  
待加密数据原长度为3字节:
  
0x410x410x41
  
填充后:
  
0x410x410x410x050x050x050x050x05
  
待加密数据原长度为4字节:
  
0x410x410x410x41
  
填充后:
  
0x410x410x410x410x040x040x040x04
  
待加密数据原长度为5字节:
  
0x410x410x410x410x41
  
填充后:
  
0x410x410x410x410x410x030x030x03
  
待加密数据原长度为6字节:
  
0x410x410x410x410x410x41
  
填充后:
  
0x410x410x410x410x410x410x020x02
  
待加密数据原长度为7字节:
  
0x410x410x410x410x410x410x41
  
填充后:
  
0x410x410x410x410x410x410x410x01
  
待加密数据原长度为8字节:
  
0x410x410x410x410x410x410x410x41
  
填充后:
  
0x410x410x410x410x410x410x410x410x080x080x080x080x080x080x080x08
  
假设待加密数据长度为x,那么将会在后面padding的字节数目为8-(x%8),每个padding的字节值是8-(x%8)。

特别地,当待加密数据长度x恰好是8的整数倍,也是要在后面多增加8个字节,每个字节是0x08。

给出一个PKCS#5的实现:

static size_t padding(unsigned char *src, size_t srcLen)
  
{

// PKCS#5

size_t paddNum = 8 - srcLen % 8;

    for (int i = 0; i < paddNum; ++i) {
        src[srcLen + i] = paddNum;
    }   
    return srcLen + paddNum;

}
  
思考一个问题:

为啥当为整数倍时,还是要多增加8个0x08？

因为解密的需要。

假设当x是8的整数倍时,不多填充8个0x08:

当解密后时,我看到了解密后的数据的末尾的最后一个字节,这个字节恰好是0x01,那你说,这个字节是填充上去的呢？

还是实际的数据呢？

类似的例子比如: 解密后末尾的两个字节恰好都是0x02,你说是填充上去的还是原来实际的明文数据？

如果我们不论是不是8的整数倍,都进行填充,那么显然可以统一进行处理！

有点绕…可以仔细想想。

PKCS#5以及PKCS#7的区别

网上关于这个问题有很多讨论。

以下是我从网上找的资料:

wiki:

Padding is in whole bytes. The value of each added byte is the number of bytes that are added, i.e. N bytes, each of value N are added. The number of bytes added will depend on the block boundary to which the message needs to be extended.

The padding will be one of:

02 02
  
03 03 03
  
04 04 04 04
  
05 05 05 05 05
  
06 06 06 06 06 06
  
etc.

This padding method (as well as the previous two) is well-defined if and only if N is less than 256.

Example: In the following example the block size is 8 bytes and padding is required for 4 bytes

... | DD DD DD DD DD DD DD DD | DD DD DD DD 04 04 04 04 |

If the original data is an integer multiple of N bytes, then an extra block of bytes with value N is added. This is necessary so the deciphering algorithm can determine with certainty whether the last byte of the last block is a pad byte indicating the number of padding bytes added or part of the plaintext message. Consider a plaintext message that is an integer multiple of N bytes with the last byte of plaintext being 01. With no additional information, the deciphering algorithm will not be able to determine whether the last byte is a plaintext byte or a pad byte. However, by adding N bytes each of value N after the 01 plaintext byte, the deciphering algorithm can always treat the last byte as a pad byte and strip the appropriate number of pad bytes off the end of the ciphertext; said number of bytes to be stripped based on the value of the last byte.
  
其实最核心的是:

PKCS#5在填充方面,是PKCS#7的一个子集:

PKCS#5只是对于8字节 (BlockSize=8) 进行填充,填充内容为0x01-0x08；

但是PKCS#7不仅仅是对8字节填充,其BlockSize范围是1-255字节。

所以,PKCS#5可以向上转换为PKCS#7,但是PKCS#7不一定可以转换到PKCS#5 (用PKCS#7填充加密的密文,用PKCS#5解出来是错误的) 。

PKCS#5 padding is identical to PKCS#7 padding, except that it has only been defined for block ciphers that use a 64-bit (8 byte) block size. In practice the two can be used interchangeably
  
再给出一个老外的答案:

The difference between the PKCS#5 and PKCS#7 padding mechanisms is the block size; PKCS#5 padding is defined for 8-byte block sizes, PKCS#7 padding would work for any block size from 1 to 255 bytes.

This is the definition of PKCS#5 padding (6.2) as defined in the RFC:

The padding string PS shall consist of 8 - (||M|| mod 8) octets all having value 8 - (||M|| mod 8).

The RFC that contains the PKCS#7 standard is the same except that it allows block sizes up to 255 bytes in size (10.3 note 2):

For such algorithms, the method shall be to pad the input at the trailing end with k - (l mod k) octets all having value k - (l mod k), where l is the length of the input.

So fundamentally PKCS#5 padding is a subset of PKCS#7 padding for 8 byte block sizes. Hence, PKCS#5 padding can not be used for AES. PKCS#5 padding was only defined with (triple) DES operation in mind.

Many cryptographic libraries use an identifier indicating PKCS#5 or PKCS#7 to define the same padding mechanism. The identifier should indicate PKCS#7 if block sizes other than 8 are used within the calculation. Some cryptographic libraries such as the SUN provider in Java indicate PKCS#5 where PKCS#7 should be used - "PKCS5Padding" should have been "PKCS7Padding". This is a legacy from the time that only 8 byte block ciphers such as (triple) DES symmetric cipher were available.

Note that neither PKCS#5 nor PKCS#7 is a standard created to describe a padding mechanism. The padding part is only a small subset of the defined functionality. PKCS#5 is a standard for Password Based Encryption or PBE, and PKCS#7 defines the Cryptographic Message Syntax or CMS.
  
资料来源:

1.<https://en.wikipedia.org/wiki/Padding_(cryptography>)

2.<https://en.wikipedia.org/wiki/PKCS>

3.<https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation>

4.<https://crypto.stackexchange.com/questions/9043/what-is-the-difference-between-pkcs5-padding-and-pkcs7-padding>

5.<http://www.cnblogs.com/ryq2014/p/6379153.html>

6.<http://blog.csdn.net/zsy19881226/article/details/46928177>
