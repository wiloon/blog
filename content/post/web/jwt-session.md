---
author: "-"
date: "2020-05-23T05:42:35Z"
lastmod: 2026-07-02T17:52:45+08:00
title: "JWT vs Session：认证方式对比"
url: jwt-session
categories:
  - Web
tags:
  - jwt
  - session
  - authentication
  - security
  - remix
  - AI-assisted
---
## 背景知识

>github.com/golang-jwt/jwt

### Authentication 和 Authorization 的区别

Authentication: 认证，指的是验证用户的身份，例如你希望以 A 的身份登录，那么应用程序需要通过用户名和密码确认你真的是 A 。

Authorization: 授权，指的是确认你的身份之后提供给你权限，例如用户 A 可以修改数据，而用户 B 只能阅读数据。

由于 http 协议是无状态的，每一次请求都无状态。当一个用户通过用户名和密码登录了之后，他的下一个请求不会携带任何状态，应用程序无法知道他的身份，那就必须重新认证。因此我们希望用户登录成功之后的每一次 HTTP 请求，都能够保存他的登录状态。

目前主流的用户认证方法有基于 token 和基于 session 两种方式，常见的还有三种细分形态：

- **无状态 JWT (Stateless JWT)**：包含 Session 数据的 JWT Token，Session 数据直接编码进 Token 内。
- **有状态 JWT (Stateful JWT)**：包含 Session 引用或其 ID 的 JWT Token，Session 数据存储在服务端。
- **Session token（又称 Session cookie）**：标准的、可被签名的 Session ID，例如各类 Web 框架 (译者注: 包括 Laravel) 内已经使用了很久的 Session 机制，Session 数据同样存储在服务端。

> 以上背景知识整理自 Wi1dcard 的文章，原文地址：[https://learnku.com/articles/22616](https://learnku.com/articles/22616)（版权归原作者所有，商业转载请联系作者获得授权）。

## Session vs JWT 详解

> 以下内容整理自 chengkai 的文章《聊一聊JWT与session》，原文地址：[https://juejin.cn/post/6844903542449242126](https://juejin.cn/post/6844903542449242126)（版权归原作者所有）。

认证和授权，简单来说：认证就是让服务器知道你是谁，授权就是服务器让你知道你能干什么、不能干什么。认证的常见方案有 Session-Cookie 与 JWT 两种，下面针对这两种方案展开对比。

### Session

#### Session 工作原理

当 client 通过用户名密码请求 server 并通过身份认证后，server 就会生成身份认证相关的 session 数据，并且保存在内存或者内存数据库。并将对应的 session_id 返回给 client，client 会把 session_id（可以加密签名防止篡改）保存在 cookie。此后 client 的所有请求都会附带该 session_id（默认会把 cookie 传给 server），以确定 server 是否存在对应的 session 数据、检验登录状态以及拥有什么权限，如果通过校验就正常处理，否则要求重新登录。

前端退出登录时清除 cookie；后端要强制前端重新认证时，清除或修改对应的 session。

![Session 认证流程](https://user-gold-cdn.xitu.io/2017/12/27/160984b7052cf619?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

#### 优势

- 相比 JWT，session 最大的优势就在于可以主动从服务端清除
- session 保存在服务器端，相对较为安全
- 结合 cookie 使用，较为灵活，兼容性较好

#### 弊端

- cookie + session 在跨域场景表现并不好
- 如果是分布式部署，需要做多机共享 session 机制，实现方法可将 session 存储到数据库或 Redis 中
- 基于 cookie 的机制容易被 CSRF 攻击（可通过 `SameSite`、`HttpOnly`、`Secure` 等 cookie 属性缓解，详见下文「安全性」）
- 查询 session 信息可能会有额外的存储查询开销

#### session、cookie、sessionStorage、localStorage 的区别

- **session**：主要存放在服务器端，相对安全
- **cookie**：可设置有效时间，默认是关闭浏览器后失效，主要存放在客户端，并不是很安全，可存储大小约为 4KB
- **sessionStorage**：仅在当前会话下有效，关闭页面或浏览器后被清除
- **localStorage**：除非被清除，否则永久保存

### JWT

JSON Web Token (JWT) 是一种开放标准 (RFC 7519)，它定义了一种紧凑且独立的方式，可以将各方之间的信息作为 JSON 对象进行安全传输。该信息可以验证和信任，因为是经过数字签名的。

JWT 由 `.` 分隔的三部分组成，分别是头部、有效载荷和签名。一个简单的 JWT 例子如下：

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ.ec7IVPU-ePtbdkb85IRnK4t4nUVvF2bBf8fGhJmEwSs
```

如果细致地去看，会发现这是一个分为 3 段的字符串，段与段之间用点号隔开，在 JWT 的概念中，每一段的名称分别为：

```text
Header.Payload.Signature
```

每一段都是 base64url 编码后的 JSON。**需要注意的是，标准 JWT（JWS，签名型）的 Payload 只是编码，并未加密，任何拿到 token 的人都能解码看到明文内容；只有使用 JWE（JSON Web Encryption）这种不同的规范才会真正加密 Payload。** 所以不要在 JWT Payload 里存放密码、身份证号等敏感信息。

#### Header

JWT 的 Header 通常包含两个字段，分别是：typ (type) 和 alg (algorithm)。

- `typ`：token 的类型，这里固定为 `JWT`
- `alg`：使用的 hash 算法，例如 HMAC SHA256 或者 RSA

一个简单的例子：

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

对其进行 Base64 编码后是：

```python
>>> base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}))
'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9'
```

#### Payload

JWT 中的 Payload 存储真正需要传递的信息，例如用户 ID、用户名，此外还包含发布人、过期日期等元数据。

这部分编码方式和 Header 一样，都是 Base64UrlEncode（而不是标准 Base64）：区别在于会忽略末尾的 padding（`=` 号），并将 `+`、`/` 分别替换成 `-`、`_`。

举例，Payload 是：

```json
{"user_id": "zhangsan"}
```

直接 Base64 编码的话应该是：

```python
>>> base64.urlsafe_b64encode('{"user_id":"zhangsan"}')
'eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ=='
```

去掉末尾的 `=` 号后，最终是：

```text
eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ
```

#### Signature

Signature 部分是对前面的 Header 和 Payload 进行签名，保证 Token 在传输过程中没有被篡改或损坏。除了 Header 和 Payload 之外，签名还需要一个密钥字段，完整算法为：

```text
Signature = HMACSHA256(
    base64UrlEncode(header) + "." + base64UrlEncode(payload),
    secret)
```

还是以前面的例子为例：

```text
base64UrlEncode(header)  => eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9
base64UrlEncode(payload) => eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ
```

secret 设为 `"secret"`，最后算出的签名是：

```python
>>> import hmac
>>> import hashlib
>>> import base64
>>> msg = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ"
>>> dig = hmac.new(b"secret", msg.encode(), hashlib.sha256)
>>> base64.urlsafe_b64encode(dig.digest())
b'ec7IVPU-ePtbdkb85IRnK4t4nUVvF2bBf8fGhJmEwSs='
```

将上面三部分组装起来就组成了 JWT token，所以 `{'user_id': 'zhangsan'}` 的 token 就是：

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiemhhbmdzYW4ifQ.ec7IVPU-ePtbdkb85IRnK4t4nUVvF2bBf8fGhJmEwSs
```

#### JWT 工作原理

1. 前端通过 Web 表单将用户名和密码发送到后端接口，一般是一个 HTTP POST 请求。建议通过 SSL 加密传输 (https 协议)，避免敏感信息被嗅探。
2. 后端核对用户名和密码成功后，将用户 id 等信息作为 JWT Payload（负载），与 Header 分别进行 Base64 编码、拼接后签名，形成一个 JWT，格式类似 `lll.zzz.xxx`。
3. 后端将 JWT 字符串作为登录成功的返回结果返回给前端。前端可以将结果保存在 `localStorage` 或 `sessionStorage` 中，退出登录时删除保存的 JWT 即可。
4. 前端在每次请求时将 JWT 放入 HTTP Header 的 `Authorization` 字段。
5. 后端检查 JWT 是否存在并验证其有效性：检查签名是否正确、Token 是否过期、Token 的接收方是否是自己（可选）。
6. 验证通过后，后端使用 JWT 中包含的用户信息进行后续逻辑处理，返回相应结果。

![JWT 认证流程](https://user-gold-cdn.xitu.io/2017/12/27/1609867a8c834efe?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

### JWTs vs. Sessions

#### 可扩展性

随着应用程序的扩大和用户数量的增加，你必将开始水平或垂直扩展。session数据通过文件或数据库存储在服务器的内存中。在水平扩展方案中，你必须开始复制服务器数据，你必须创建一个独立的中央session存储系统，以便所有应用程序服务器都可以访问。否则，由于session存储的缺陷，你将无法扩展应用程序。解决这个挑战的另一种方法是使用 sticky session。你还可以将session存储在磁盘上，使你的应用程序在云环境中轻松扩展。这类解决方法在现代大型应用中并没有真正发挥作用。建立和维护这种分布式系统涉及到深层次的技术知识，并随之产生更高的财务成本。在这种情况下，使用JWT是无缝的;由于基于token的身份验证是无状态的，所以不需要在session中存储用户信息。我们的应用程序可以轻松扩展，因为我们可以使用token从不同的服务器访问资源，而不用担心用户是否真的登录到某台服务器上。你也可以节省成本，因为你不需要专门的服务器来存储session。为什么？因为没有session！

注意: 如果你正在构建一个小型应用程序，这个程序完全不需要在多台服务器上扩展，并且不需要RESTful API的，那么session机制是很棒的。 如果你使用专用服务器运行像Redis那样的工具来存储session，那么session也可能会为你完美地运作！

#### 安全性

JWT 签名可以防止在客户端被篡改；如果需要保密还可以额外使用 JWE 加密。JWT 常被直接存储在 Web 存储 (localStorage/sessionStorage) 或 cookie 中。JavaScript 可以访问同一个域上的 Web 存储，这意味着 JWT 可能容易受到 XSS（跨站脚本）攻击——恶意 JavaScript 一旦被嵌入页面，就能读取和篡改 Web 存储的内容。因此不应该在 JWT 中编码过于敏感的数据，例如身份证号、社会安全号码等。

JWT 也常被存储为 cookie，而 cookie 容易受到 CSRF（跨站请求伪造）攻击。具体的缓解手段包括：

- cookie 设置 `HttpOnly`，禁止 JavaScript 读取，缓解 XSS 窃取 token
- cookie 设置 `Secure`，只在 HTTPS 下传输
- cookie 设置 `SameSite=Strict` 或 `Lax`，减少跨站请求携带 cookie 的风险
- 服务端额外校验 CSRF Token（双重提交 cookie 等机制）

不管是否使用 JWT，作为开发者都要确保上述 CSRF/XSS 防护措施到位。CSRF 攻击的完整原理和案例见 [CSRF/XSRF](./csrfxsrf.md)。

JWT 和 session ID 同样会暴露于未经防范的重放攻击，具体防护技术取决于系统设计，例如缩短 JWT 的过期时间（无法完全解决问题），或将 JWT 与特定 IP、设备指纹绑定。

注意：使用 HTTPS/SSL 确保 Cookie 和 JWT 在客户端与服务器传输期间加密，避免中间人攻击。

#### RESTful API服务

现代应用程序的常见模式是从RESTful API查询使用JSON数据。目前大多数应用程序都有RESTful API供其他开发人员或应用程序使用。由API提供的数据具有几个明显的优点，其中之一就是这些数据可以被多个应用程序使用。在这种情况下，传统的使用session和Cookie的方法在用户认证方面效果不佳，因为它们将状态引入到应用程序中。

RESTful API的原则之一是它应该是无状态的，这意味着当发出请求时，总会返回带有参数的响应，不会产生附加影响。用户的认证状态引入这种附加影响，这破坏了这一原则。保持API无状态，不产生附加影响，意味着维护和调试变得更加容易。

另一个挑战是，由一个服务器提供API，而实际应用程序从另一个服务器调用它的模式是很常见的。为了实现这一点，我们需要启用跨域资源共享 (CORS) 。Cookie只能用于其发起的域，相对于应用程序，对不同域的API来说，帮助不大。在这种情况下使用JWT进行身份验证可以确保RESTful API是无状态的，你也不用担心API或应用程序由谁提供服务。

#### 性能

对此的批判性分析是非常必要的。当从客户端向服务器发出请求时，如果大量数据在JWT内进行编码，则每个HTTP请求都会产生大量的开销。然而，在会话中，只有少量的开销，因为SESSION ID实际上非常小。看下面这个例子:

JWT有5个claim:

```json
{
  "sub": "1234567890",
  "name": "Prosper Otemuyiwa",
  "admin": true,
  "role": "manager",
  "company": "Auth0"
}
```

编码时，JWT的大小将是SESSION ID (标识符) 的几倍，从而在每个HTTP请求中，JWT比SESSION ID增加更多的开销。而对于session，每个请求在服务器上需要查找和反序列化session。

JWT通过将数据保留在客户端的方式以空间换时间。你应用程序的数据模型是一个重要的影响因素，因为通过防止对服务器数据库不间断的调用和查询来减少延迟。需要注意的是不要在JWT中存储太多的claim，以避免发生巨大的，过度膨胀的请求。

值得一提的是，token可能需要访问后端的数据库。特别是刷新token的情况。他们可能需要访问授权服务器上的数据库以进行黑名单处理。另外，请查看本文，了解有关黑名单的更多信息（[auth0.com/blog/blackl…](https://auth0.com/blog/blacklist-json-web-token-api-keys/)）。

#### 下游服务

现代web应用程序的另一种常见模式是，它们通常依赖于下游服务。例如，在原始请求被解析之前，对主应用服务器的调用可能会向下游服务器发出请求。这里的问题是，cookie不能很方便地流到下游服务器，也不能告诉这些服务器关于用户的身份验证状态。由于每个服务器都有自己的cookie方案，所以阻力很大，并且连接它们也是困难的。JSON Web Token再次轻而易举地做到了！

#### 实效性

此外，无状态JWT的实效性相比session太差，只有等到过期才可销毁，而session则可手动销毁。

例如有个这种场景，如果JWT中存储有权限相关信息，比如当前角色为 admin，但是由于JWT所有者滥用自身权利，高级管理员将权利滥用者的角色降为 user。但是由于 JWT 无法实时刷新，必需要等到 JWT 过期，强制重新登录时，高级管理员的设置才能生效。

或者是用户发现账号被异地登录，然后修改密码，此时token还未过期，异地的账号一样可以进行操作包括修改密码。

但这种场景也不是没有办法解决，解决办法就是将JWT生成的token存入到redis或者数据库中，当用户登出或作出其他想要让token失效的举动，可通过删除token在数据库或者redis里面的对应关系来解决这个问题。

### Node.js 中使用 JWT

以 Node.js 为例，使用 `jsonwebtoken` 库的方式如下：

安装依赖：

```bash
npm install jsonwebtoken
```

创建签名数据，生成 token：

```javascript
let jwt = require('jsonwebtoken');

var token = jwt.sign({ name: '张三' }, 'shhhhh');
console.log(token);
```

运行程序会打印出类似这样的内容：

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoi5byg5LiJIiwiaWF0IjoxNDYyODgxNDM3fQ.uVWC2h0_r1F4FZ3qDLkGN5KoFYbyZrFpRJMONZrJJog
```

之后，对 token 字符串，可以这样解码：

```javascript
let decoded = jwt.decode(token);
console.log(decoded);
```

将打印出：

```text
{ name: '张三', iat: 1462881437 }
```

其中 `iat` 是时间戳，即签名时间（单位是秒）。

不过一般不会使用 `decode` 方法，因为它只是对 claims 部分做简单的 base64 解码，并不校验内容是否被篡改。真正需要验证 claims 内容时要使用 `verify` 方法：

```javascript
let decoded = jwt.verify(token, 'shhhhh');
console.log(decoded);
```

打印出的内容和 `decode` 方法一样，但这次是经过签名校验的。

如果改变校验用的密钥（比如改为 `shzzzz`），使之和加密时的密钥不一致，解码就会报错：

```text
JsonWebTokenError: invalid signature
```

如果偷偷修改 token 的 claims 或 header 部分，也会得到类似的报错：

```text
JsonWebTokenError: invalid token
```

最后，根据自己的需求决定是否需要将生成的 token 存入数据库或 Redis，但不建议存储用户密码等敏感信息。

### 对比总结

| 维度 | Session | JWT |
| ---- | ------- | --- |
| 存储位置 | 服务端（内存/DB/Redis），客户端仅存 session_id | 客户端（cookie/localStorage/sessionStorage），服务端可不存储 |
| 扩展性 | 分布式部署需要共享 session（DB/Redis/sticky session） | 无状态，天然适合水平扩展和多服务器场景 |
| 主动失效 | 可随时在服务端删除/修改 session | 默认只能等过期；需要主动失效则要引入服务端黑名单（Redis/DB） |
| 跨域/多服务 | Cookie 默认不跨域，下游服务共享状态较麻烦 | 可放入 Authorization Header，天然适合跨域、微服务、开放 API |
| 常见攻击面 | CSRF（cookie 自动携带） | XSS（token 存在 Web 存储中易被读取）；作为 cookie 存储时同样有 CSRF 风险 |
| 单次请求开销 | 小（仅 session_id），但每次要查库/查缓存 | 更大（携带全部 claim），但省去服务端查询 |

**选型建议**：

- 单体应用、服务端渲染、不需要跨多个服务共享认证状态 → **Session** 更简单可靠，且能随时强制下线。
- 无状态多实例部署、面向移动端/第三方开放 API、需要跨域或跨多个下游服务传递身份 → **JWT** 更合适。
- 既想要 JWT 的无状态优势，又需要「主动踢人下线」的能力 → 折中方案：**有状态 JWT / JWT + Redis 黑名单**（登出或强制失效时把 token 写入黑名单，网关校验时排除黑名单中的 token），或采用短期 access token + 可撤销的 refresh token（见下文「Refresh Token 相关阅读」）。

关于安全的 cookie 属性（`HttpOnly`/`Secure`/`SameSite`）等更多细节，见上文「安全性」小节。

### Refresh Token 相关阅读

站内相关文章：[Refresh Token Rotation: 刷新令牌轮换与重放检测](./refresh-token-rotation.md)、[OAuth2.0](./oauth2-0.md)。

站外参考：

- [https://zhuanlan.zhihu.com/p/52300092](https://zhuanlan.zhihu.com/p/52300092)
- [https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/#silent_refresh](https://hasura.io/blog/best-practices-of-using-jwt-with-graphql/#silent_refresh)
- [https://usthe.com/2018/04/%E7%AD%BE%E5%8F%91%E7%9A%84%E7%94%A8%E6%88%B7%E8%AE%A4%E8%AF%81token%E8%B6%85%E6%97%B6%E5%88%B7%E6%96%B0%E7%AD%96%E7%95%A5/](https://usthe.com/2018/04/%E7%AD%BE%E5%8F%91%E7%9A%84%E7%94%A8%E6%88%B7%E8%AE%A4%E8%AF%81token%E8%B6%85%E6%97%B6%E5%88%B7%E6%96%B0%E7%AD%96%E7%95%A5/)
- [https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)

所以... JWT 适合做什么？
在本文之初，我就提到 JWT 虽然不适合作为 Session 机制，但在其它方面的确有它的用武之地。该主张依旧成立，JWT 特别有效的使用例子通常是作为一次性的授权令牌。

引用 JSON Web Token specification:

JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties.  enabling the claims to be digitally signed or integrity protected with a Message Authentication Code (MAC) and/or encrypted.

在此上下文中，「Claim」可能是一条「命令」，一次性的认证，或是基本上能够用以下句子描述的任何情况:

你好，服务器 B，服务器 A 告诉我我可以 <...Claim...>，这是我的证据: < ... 密钥... >。

举个例子，你有个文件服务，用户必须认证后才能下载文件，但文件本身存储在一台完全分离且无状态的「下载服务器」内。在这种情况下，你可能想要「应用服务器 (服务器 A) 」颁发一次性的「下载 Tokens」，用户能够使用它去「下载服务器 (服务器 B) 」获取需要的文件。

以这种方式使用 JWT，具备几个明确的特性：

- Tokens 生命期较短。它们只需在几分钟内可用，让客户端能够开始下载。
- Tokens 仅单次使用。应用服务器应当在每次下载时颁发新的 Token。所以任何 Token 只用于一次请求就会被抛弃，不存在任何持久化的状态。
- 应用服务器依旧使用 Sessions。仅仅下载服务器使用 Tokens 来授权每次下载，因为它不需要任何持久化状态。

正如以上你所看到的，结合 Sessions 和 JWT Tokens 有理有据。它们分别拥有各自的目的，有时候你需要两者一起使用。只是不要把 JWT 用作持久的、长期的数据就好。

---

[https://learnku.com/articles/22616](https://learnku.com/articles/22616)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-02 | 补全 front matter（url、lastmod，修正 title/categories）；标签由 reprint 改为 remix + AI-assisted；清理开头重复/错位片段与二次引用说明；修正标题层级跳级（##### → ####）；代码块改为围栏代码块并补充语言标识，移除残留的“复制代码”文字；修复 HMAC 签名示例代码错误；澄清 JWT Payload 是编码而非加密；补充 HttpOnly/SameSite/Secure cookie 属性说明及指向 CSRF/XSRF 的站内链接；新增 JWT 与 Session 对比总结表及站内相关文章链接 | 原文档为两篇转载文章直接拼接，存在格式错误、内容重复、代码不可运行及部分技术表述不准确的问题 |
