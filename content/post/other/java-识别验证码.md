---
title: 短信验证码
author: "-"
date: 2012-09-30T02:29:19+00:00
url: /?p=4352
categories:
  - inbox
tags:
  - reprint
---
## 短信验证码



- 短信验证码有效期2分钟
- 验证码 6 位纯数字 
- 每个手机号60秒内只能发一次短信验证码, 前后端都要做验证
- 同一个手机号在同一时间可以有多个有效的验证码
- 验证码不记录到日志
- 验证码使用后作废 (使用后作废,不太友好,如果有其它信息填写错误得等1分钟再重新取验证码)
- 验证码至多可以使用3次,无论是否匹配都作废,防止暴力攻击 (一个手机号验证三次之后, 作废关联的验证码)


### java 识别验证码
<http://blog.csdn.net/problc/article/details/5800093>

---

https://www.cnblogs.com/guokun/p/11042903.html
https://insights.thoughtworks.cn/sms-authentication-login-api/
