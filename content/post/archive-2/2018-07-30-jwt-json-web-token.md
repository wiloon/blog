---
title: JWT JSON Web Token
author: wiloon
type: post
date: 2018-07-30T12:02:39+00:00
url: /?p=12462
categories:
  - Uncategorized

---
http://blog.leapoahead.com/2015/09/06/understanding-jwt/

JSON Web Token (JWT)是一种基于 token 的认证方案。

JSON Web Token 的结构

一个 JWT token 看起来是这样的:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.

eyJleHAiOjEzODY4OTkxMzEsImlzcyI6ImppcmE6MTU0ODk1OTUiLCJxc2

giOiI4MDYzZmY0Y2ExZTQxZGY3YmM5MGM4YWI2ZDBmNjIwN2Q0OTFjZj

ZkYWQ3YzY2ZWE3OTdiNDYxNGI3MTkyMmU5IiwiaWF0IjoxMzg2ODk4OTUxfQ.

uKqU9dTB6gKwG6jQCuXYAiMNdfNRw98Hw_IWuA5MaMo

可以简化为下面这样的结构:

base64url\_encode(Header) + &#8216;.&#8217; + base64url\_encode(Claims) + &#8216;.&#8217; + base64url_encode(Signature)

Header

Header 包含了一些元数据，至少会表明 token 类型以及 签名方法。比如

{

"typ&#8221; : "JWT&#8221;,

"alg&#8221; : "HS256&#8221;

}

type: 必需。token 类型，JWT表示是 JSON Web Token.

alg: 必需。token 所使用的签名算法，可用的值在这里有规定。

Claims (Payload)

Claims 部分包含了一些跟这个 token 有关的重要信息。 JWT 标准规定了一些字段，下面节选一些字段:

iss: The issuer of the token，token 是给谁的

sub: The subject of the token，token 主题

exp: Expiration Time。 token 过期时间，Unix 时间戳格式

iat: Issued At。 token 创建时间， Unix 时间戳格式

jti: JWT ID。针对当前 token 的唯一标识

https://www.jianshu.com/p/15572dfa4ccd

http://blog.leapoahead.com/2015/09/06/understanding-jwt/

JWT（其实还有SAML）最适合的应用场景就是“开票”，或者“签字”。

在有纸化办公时代，多部门、多组织之间的协同工作往往会需要拿着A部门领导的“签字”或者“盖章”去B部门“使用”或者“访问”对应的资源，其实这种“领导签字／盖章”就是JWT，都是一种由具有一定权力的实体“签发”并“授权”的“票据”。一般的，这种票据具有可验证性（领导签名／盖章可以被验证，且难于模仿），不可篡改性（涂改过的文件不被接受，除非在涂改处再次签字确认）；并且这种票据一般都是“一次性”使用的，在访问到对应的资源后，该票据一般会被资源持有方收回留底，用于后续的审计、追溯等用途。

举两个例子：

员工李雷需要请假一天，于是填写请假申请单，李雷在获得其主管部门领导签字后，将请假单交给HR部门韩梅梅，韩梅梅确认领导签字无误后，将请假单收回，并在公司考勤表中做相应记录。
  
员工李雷和韩梅梅因工外出需要使用公司汽车一天，于是填写用车申请单，签字后李雷将申请单交给车队司机老王，乘坐老王驾驶的车辆外出办事，同时老王将用车申请单收回并存档。
  
在以上的两个例子中，“请假申请单”和“用车申请单”就是JWT中的payload，领导签字就是base64后的数字签名，领导是issuer，“HR部门的韩梅梅”和“司机老王”即为JWT的audience，audience需要验证领导签名是否合法，验证合法后根据payload中请求的资源给予相应的权限，同时将JWT收回。