---
title: Bcrypt
author: "-"
date: 2019-04-30T04:11:41+00:00
url: bcrypt
categories:
  - Security
tags:
  - reprint
---
## Bcrypt
https://www.jianshu.com/p/2b131bfc2f10
  
Bcrypt 是单向Hash加密算法，类似 Pbkdf2 算法 不可反向破解生成明文。 每次输出的hashPass 都不一样，
  
## Bcrypt是怎么加密的？
  
Bcrypt有四个变量: 

saltRounds: 正数，代表hash杂凑次数，数值越高越安全，默认10次。
  
myPassword: 明文密码字符串。
  
salt: 盐，一个128bits随机字符串，22字符
  
myHash: 经过明文密码password和盐salt进行hash，个人的理解是默认10次下 ，循环加盐hash10次，得到myHash

每次明文字符串myPassword过来，就通过10次循环加盐salt加密后得到myHash, 然后拼接BCrypt版本号+salt盐+myHash等到最终的bcrypt密码 ，存入数据库中。
  
这样同一个密码，每次登录都可以根据自省业务需要生成不同的myHash, myHash中包含了版本和salt，存入数据库。

作者: martin6699
  
链接: https://www.jianshu.com/p/2b131bfc2f10
  
来源: 简书
  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

>https://www.ujcms.com/knowledge/509.html
>http://www.mindrot.org/projects/jBCrypt/
>https://www.cnblogs.com/jpfss/p/11024716.html
>http://www.mindrot.org/projects/jBCrypt/


### 在 Java 中使用 Bcrypt, BCryptPasswordEncoder
如果引入了 Spring Security, BCryptPasswordEncoder 提供了相关的方法。

```java
public class BCryptPasswordEncoderTest {
    public static void main(String[] args) {
        String pass = "admin";
        BCryptPasswordEncoder bcryptPasswordEncoder = new BCryptPasswordEncoder();
        String hashPass = bcryptPasswordEncoder.encode(pass);
        System.out.println(hashPass);

        boolean f = bcryptPasswordEncoder.matches("admin",hashPass);
        System.out.println(f);

    }
}
```
可以看到，每次输出的hashPass 都不一样，
但是最终的f都为 true,即匹配成功。

查看代码，可以看到，其实每次的随机盐，都保存在hashPass中。

在进行matchs进行比较时，调用BCrypt 的String hashpw(String password, String salt)

方法。两个参数即”admin“和 hashPass

```java
//******BCrypt.java******salt即取出要比较的DB中的密码*******
real_salt = salt.substring(off + 3, off + 25);
try {
// ***************************************************
    passwordb = (password + (minor >= 'a' ? "\000" : "")).getBytes("UTF-8");
}
catch (UnsupportedEncodingException uee) {}
saltb = decode_base64(real_salt, BCRYPT_SALT_LEN);
B = new BCrypt();
hashed = B.crypt_raw(passwordb, saltb, rounds);
```
假定一次hashPass为：$2a$10$AxafsyVqK51p.s9WAEYWYeIY9TKEoG83LTEOSB3KUkoLtGsBKhCwe

随机盐即为 AxafsyVqK51p.s9WAEYWYe

 (salt = BCrypt.gensalt();中有描述）

可见，随机盐 (AxafsyVqK51p.s9WAEYWYe），会在比较的时候，重新被取出。

即，加密的hashPass中，前部分已经包含了盐信息。

>https://zhuanlan.zhihu.com/p/92845975
>https://www.cnblogs.com/jpfss/p/11023906.html
