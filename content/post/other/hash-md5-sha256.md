---
title: md5, sha256
author: "-"
date: 2011-10-14T06:35:16+00:00
url: md5
categories:
  - Development
  - Linux
tags:$
  - reprint
---
## md5, sha256

```bash
#linux
md5sum [OPTION]... [FILE]...
md5sum foo.tar
sha256sum foo.tar
sha1sum foo.tar

#windows
certutil -hashfile foo.tar MD5
certutil -hashfile foo.tar SHA1
certutil -hashfile foo.tar SHA256
```

MD5: 一种单向Hash函数/单向散列函数

Message Digest Algorithm MD5 (中文名为消息摘要算法第五版) 为计算机安全领域广泛使用的一种散列函数，用以提供消息的完整性保护。该算法的文件号为RFC 1321 (R.Rivest,MIT Laboratory for Computer Science and RSA Data Security Inc. April 1992) 。
 
### 描述
MD5算法常常被用来验证网络文件传输的完整性，防止文件被人篡改。MD5 全称是报文摘要算法 (Message-Digest Algorithm 5) ，此算法对任意长度的信息逐位进行计算，产生一个二进制长度为128位 (十六进制长度就是32位) 的"指纹" (或称"报文摘要") ，不同的文件产生相同的报文摘要的可能性是非常非常之小的。
  
在linux或Unix上，md5sum是用来计算和校验文件报文摘要的工具程序。一般来说，安装了Linux后，就会有md5sum这个工具，直接在命令行终端直接运行。
  
选项:

    -b 或 -binary :把输入文件作为二进制文件看待。
    -t 或 -text :把输入的文件作为文本文件看待 (默认) 。
    -c 或 -check :用来从文件中读取md5信息检查文件的一致性。(不细说了参见info)
    -status :这个选项和check一起使用,在check的时候，不输出，而是根据返回值表示检查结果。
    -w 或 -warn :在check的时候，检查输入的md5信息又没有非法的行，如果有则输出相应信息。

[举例]
  
1>生成一个文件testfile的md5值: 

$ md5sum testfile
  
输入之后，输出类似如下: 
  
661b2da42057527f30cff69fe466ebeb testfile
  
这里，如果我拷贝一份testfile成testfile.copy那么生成的md5值是一样的，但是我如果修改了testfile.copy的内容，那么就不一样了，如果再把修改的内容恢复回去，再保存testfile.copy那么生成的md5值又一样了。注意，可以输入多个文件，分别生成每个文件的md5,但是目录不能是输入文件。
  
2>把testfile做为二进制文件生成md5值:

$ md5sum -b testfile
  
输入之后，输出如下: 
  
661b2da42057527f30cff69fe466ebeb *testfile
  
这里和前面的结果一样，不过文件名称前面有一个testfile.
  
3>检查文件testfile是否被修改过: 

1)首先生成md5文件: 
  
$md5sum testfile >testfile.md5
  
2)检查: 
  
$md5sum testfile -c testfile.md5
  
如果文件没有变化，输出应该如下: 
  
forsort: OK
  
此时，md5sum命令返回0。
  
如果文件发生了变化，输出应该如下: 
  
forsort: FAILED
  
md5sum: WARNING: 1 of 1 computed checksum did NOT match
  
此时，md5sum命令返回非0。
  
这里，检查用的文件名随意。如果不想有任何输出，则"md5sum testfile -status -c testfile.md5",这时候通过返回值来检测结果。

检测的时候如果检测文件非法则输出信息的选项:
  
$ md5sum -w -c testfile.md5
  
输出之后，文件异常输出类似如下: 
  
md5sum: testfile.md5: 1: improperly formatted MD5 checksum line
  
md5sum: testfile.md5: no properly formatted MD5 checksum lines found
  
这里，testfile.md5只有一行信息，但是我认为地给它多加了一个字符，导致非法。如果md5文件正常那么-w有没有都一样。


### java md5
```java    public static String getMD5Str(String str) throws Exception {
        try {
            // 生成一个MD5加密计算摘要
            MessageDigest md = MessageDigest.getInstance("MD5");
            // 计算md5函数
            md.update(str.getBytes());
            // digest()最后确定返回md5 hash值，返回值为8为字符串。因为md5 hash值是16位的hex值，实际上就是8位的字符
            // BigInteger函数则将8位的字符串转换成16位hex值，用字符串来表示；得到字符串形式的hash值
            return new BigInteger(1, md.digest()).toString(16);
        } catch (Exception e) {
            throw new Exception("MD5加密出现错误，"+e.toString());
        }

```

### 单向散列函数的性质
- 根据任意长度的信息计算固定长度的散列值
- 快速计算散列值
- 消息不同散列值不同(ps:现在貌似有不同的消息有相同的散列值)
- 具备单向性(也就是通过散列值不能反算出消息来)

### 实际应用
- 检测软件是否篡改
- 基于口令的加密(密码+salt后在进行散列计算,存储后可以防止字典攻击)
- 消息认证码
- 数字签名
- 伪随机生成器
- 一次性口令

### 具体函数
- MD4,MD5(已经不安全)
- SHA-1,SHA-256,SHA-3(SHA-1不安全)

### 解决问题
防篡改


### CRAM-MD5
CRAM-MD5即是一种Keyed-MD5验证方式，CRAM是“Challenge-Response Authentication Mechanism”的所写。所谓Keyed-MD5，是将Clieng与Server共享的一个Key作为一部分MD5的输入

---

http://vaqeteart.javaeye.com/blog/837914

https://zhuanlan.zhihu.com/p/26995802

