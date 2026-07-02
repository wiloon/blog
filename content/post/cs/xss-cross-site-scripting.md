---
title: XSS, Cross Site Scripting, CSRF, Cross-site request forgery, CORS
author: "-"
date: 2018-12-13T06:38:16.000+00:00
lastmod: 2026-07-02T18:20:33+08:00
url: XSS
categories:
- Web
tags:
  - xss
  - csrf
  - cors
  - security
  - remix
  - AI-assisted
---
## CORS, XSS, Cross Site Scripting, CSRF, Cross-site request forgery

## CORS, Cross-Origin Resource Sharing, 跨源资源共享, 跨域资源共享

CORS (Cross-Origin Resource Sharing，跨源资源共享) 是一种基于 HTTP 头的机制,允许服务器指示浏览器应该允许哪些源(域、协议或端口)来访问其资源。

### 核心概念

1. 同源策略 (Same-Origin Policy)
同源策略是浏览器最核心的安全机制之一,用于隔离潜在的恶意文档,防止不同源的网页之间互相干扰。
默认情况下, 网页只能请求与自身同源的资源。

什么是"同源":

两个 URL 只有在以下三个部分完全相同时才被认为是同源的:

协议 (Protocol): http/https
域名 (Domain): 包括子域名
端口 (Port): 默认端口可省略

假设当前页面是: http://www.example.com:80/dir/page.html

http://www.example.com/dir2/other.html	        ✅ 同源	    协议、域名、端口相同
http://www.example.com:80/dir/inner/page.html	✅ 同源	    80 是 http 默认端口
https://www.example.com/page.html	            ❌ 不同源	协议不同 (https vs http)
http://www.example.com:8080/page.html	        ❌ 不同源	端口不同 (8080 vs 80)
http://api.example.com/page.html	            ❌ 不同源	域名不同 (子域名不同)
http://example.com/page.html	                ❌ 不同源	域名不同 (缺少 www)

### 同源策略的限制范围

1. DOM 访问限制
不同源的网页不能通过 JavaScript 访问对方的 DOM:

```bash
// 页面 A: http://example.com
// 页面 B: http://other.com (在 iframe 中)
const iframe = document.getElementById('myIframe');
iframe.contentWindow.document; // ❌ 跨域访问被阻止
```

2. Cookie、LocalStorage、IndexedDB 访问限制
不同源的页面无法读取对方的存储数据:

3. AJAX 请求限制
不同源的 AJAX 请求会被浏览器阻止(除非服务器配置 CORS):

```javascript
fetch('http://api.other.com/data')
  .then(res => res.json())
  .catch(err => {
    // ❌ CORS error: 跨域请求被阻止
    console.error(err);
  });
```

不受同源策略限制的情况
以下资源可以跨域加载:

<script> 标签: <script src="http://other.com/script.js"></script>
<link> 标签: <link href="http://other.com/style.css">
<img> 标签: <img src="http://other.com/image.jpg">
<video> 和 <audio> 标签
<iframe> 标签: 可以嵌入,但无法访问内容
@font-face 字体文件
表单提交: <form action="http://other.com/submit">


2. 跨域问题
当前端代码(如 https://example.com)需要请求不同源的 API(如 https://api.other.com)时,浏览器会阻止这个请求。

3. CORS 的作用
CORS 提供了一种安全的方式来突破同源策略的限制,允许服务器明确声明哪些外部源可以访问其资源。

由于现实使用中，很多需要跨域访问，所以 W3C 标准就提出了 CORS。

跨域资源共享(CORS) 是一种机制，它使用额外的 HTTP 头来告诉浏览器 让运行在一个 origin (domain) 上的 Web 应用被准许访问来自不同源服务器上的指定的资源。当一个资源从与该资源本身所在的服务器不同的域、协议或端口请求一个资源时，资源会发起一个跨域 HTTP 请求。

具体查看官方文档：[https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS)
[https://tech.meituan.com/2018/09/27/fe-security.html](https://tech.meituan.com/2018/09/27/fe-security.html)
简单里的理解，就是 CORS 提供了一种设置你的页面可以访问指定的域名下的资源 (API）的方法。当然这些域名是你受信任的。从而避免了 CRSF 攻击。CORS 就像是一个过滤器。

注意：很多开发者在碰到跨域问题提时，通过搜索得到的答案就是直接设置 Origin: * 这样的结果就是你的网页信任任何域名，虽然达到了跨域访问的目的，但是同时失去了 CORS 的意义，因为你设置了这个过滤器不过滤任何域

CORS 需要浏览器和服务器同时支持。目前，所有浏览器都支持该功能，IE 浏览器不能低于 IE10。

整个 CORS 通信过程，都是浏览器自动完成，不需要用户参与。对于开发者来说，CORS 通信与同源的 AJAX 通信没有差别，代码完全一样。浏览器一旦发现 AJAX 请求跨源，就会自动添加一些附加的头信息，有时还会多出一次附加的请求，但用户不会有感觉。

因此，实现 CORS 通信的关键是服务器。只要服务器实现了 CORS 接口，就可以跨源通信。

[https://www.ruanyifeng.com/blog/2016/04/cors.html](https://www.ruanyifeng.com/blog/2016/04/cors.html)


[https://www.ruanyifeng.com/blog/2016/04/cors.html](https://www.ruanyifeng.com/blog/2016/04/cors.html)  
[https://tech.meituan.com/2018/09/27/fe-security.html](https://tech.meituan.com/2018/09/27/fe-security.html)  
[https://github.com/OWASP?page=5](https://github.com/OWASP?page=5)  

[https://github.com/owasp/java-html-sanitizer](https://github.com/owasp/java-html-sanitizer)

[https://www.owasp.org/index.php/Category:OWASP_AntiSamy_Project](https://www.owasp.org/index.php/Category:OWASP_AntiSamy_Project)

[https://mvnrepository.com/artifact/org.owasp.antisamy/antisamy](https://mvnrepository.com/artifact/org.owasp.antisamy/antisamy)

[https://github.com/GDSSecurity/AntiXSS-for-Java](https://github.com/GDSSecurity/AntiXSS-for-Java)

[https://segmentfault.com/a/1190000007059639](https://segmentfault.com/a/1190000007059639)

[https://www.freebuf.com/sectool/134015.html](https://www.freebuf.com/sectool/134015.html)

[https://blog.csdn.net/ru_li/article/details/51334082](https://blog.csdn.net/ru_li/article/details/51334082)

[https://blog.csdn.net/zer0_o/article/details/28399533](https://blog.csdn.net/zer0_o/article/details/28399533)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>title0</title>
    <!–css–>

    <!--javascript-->
    <script type="text/javascript">
        window.onload = function () {
            console.log('window.onload')
        }
        function func0(){
            // 1. Create a new XMLHttpRequest object
            let xhr = new XMLHttpRequest();

            // 2. Configure it: GET-request for the URL /article/.../load
            xhr.open('GET', 'http://localhost:8000');

            // 3. Send the request over the network
            xhr.send();

            // 4. This will be called after the response is received
            xhr.onload = function () {
                if (xhr.status !== 200) {
                    // analyze HTTP status of the response
                    console.log(`Error ${xhr.status}: ${xhr.statusText}`);
                    // e.g. 404: Not Found
                } else {
                    // show the result
                    console.log(`Done, got ${xhr.response.length} bytes`);
                    // response is the server
                }

                xhr.onprogress = function (event) {
                    if (event.lengthComputable) {
                        console.log(`Received ${event.loaded} of ${event.total} bytes`);
                    } else {
                        console.log(`Received ${event.loaded} bytes`); // no Content-Length
                    }
                };
                xhr.onerror = function () {
                    console.log("Request failed");
                };
            }
        }
    </script>
</head>
<body>
body0
<button type="button" onclick="func0()">button0</button>
</body>
</html>

```

#### Access-Control-Allow-Origin

该字段是必须的。它的值要么是请求时 Origin 字段的值，要么是一个 *，表示接受任意域名的请求。

#### Access-Control-Allow-Credentials

该字段可选。它的值是一个布尔值，表示是否允许发送Cookie。默认情况下，Cookie不包括在CORS请求之中。设为true，即表示服务器明确许可，Cookie可以包含在请求中，一起发给服务器。这个值也只能设为true，如果服务器不要浏览器发送Cookie，删除该字段即可。

 (3）Access-Control-Expose-Headers

该字段可选。CORS请求时，XMLHttpRequest对象的getResponseHeader()方法只能拿到6个基本字段：Cache-Control、Content-Language、Content-Type、Expires、Last-Modified、Pragma。如果想拿到其他字段，就必须在Access-Control-Expose-Headers里面指定。上面的例子指定，getResponseHeader('FooBar')可以返回FooBar字段的值。

3.2 withCredentials 属性
上面说到，CORS请求默认不发送Cookie和HTTP认证信息。如果要把Cookie发到服务器，一方面要服务器同意，指定Access-Control-Allow-Credentials字段。

Access-Control-Allow-Credentials: true
另一方面，开发者必须在AJAX请求中打开withCredentials属性。

var xhr = new XMLHttpRequest();
xhr.withCredentials = true;
否则，即使服务器同意发送Cookie，浏览器也不会发送。或者，服务器要求设置Cookie，浏览器也不会处理。

但是，如果省略withCredentials设置，有的浏览器还是会一起发送Cookie。这时，可以显式关闭withCredentials。

xhr.withCredentials = false;
需要注意的是，如果要发送Cookie，Access-Control-Allow-Origin就不能设为星号，必须指定明确的、与请求网页一致的域名。同时，Cookie依然遵循同源政策，只有用服务器域名设置的Cookie才会上传，其他域名的Cookie并不会上传，且 (跨源）原网页代码中的document.cookie也无法读取服务器域名下的Cookie。

>[https://www.ruanyifeng.com/blog/2016/04/cors.html](https://www.ruanyifeng.com/blog/2016/04/cors.html)


## XSS, Cross Site Scripting(CSS), CSRF, Cross-site request forgery， 跨站脚本攻击, CORS

XSS 攻击又称CSS,全称Cross Site Script   (跨站脚本攻击）,缩写为XSS。恶意攻击者往Web页面里插入恶意javaScript代码,当用户浏览该页之时,嵌入其中Web里面的javaScript代码会被执行,从而达到恶意攻击用户的目的。

什么是 XSS
Cross-Site Scripting (跨站脚本攻击）简称 XSS，是一种代码注入攻击。攻击者通过在目标网站上注入恶意脚本，使之在用户的浏览器上运行。利用这些恶意脚本，攻击者可获取用户的敏感信息如 Cookie、SessionID 等，进而危害数据安全。

为了和 CSS 区分，这里把攻击的第一个字母改成了 X，于是叫做 XSS。

XSS 的本质是：恶意代码未经过滤，与网站正常的代码混在一起；浏览器无法分辨哪些脚本是可信的，导致恶意脚本被执行。

而由于直接在用户的终端执行，恶意代码能够直接获取用户的信息，或者利用这些信息冒充用户向网站发起攻击者定义的请求。

在部分情况下，由于输入的限制，注入的恶意脚本比较短。但可以通过引入外部的脚本，并由浏览器执行，来完成比较复杂的攻击策略。

### XSS攻击的分类

1. 反射型
又称为非持久性跨站点脚本攻击。漏洞产生的原因是攻击者注入的数据反映在响应中。非持久型XSS攻击要求用户访问一个被攻击者篡改后的链接,用户访问该链接时,被植入的攻击脚本被用户流览器执行,从而达到攻击目的。也就是我上面举的那个简单的XSS攻击案例,通过url参数直接注入。然后在响应的数据中包含着危险的代码。
当黑客把这个链接发给你,你就中招啦！

2. 存储型
又称为持久型跨站点脚本,它一般发生在XSS攻击向量(一般指XSS攻击代码)存储在网站数据库,当一个页面被用户打开的时候执行。持久的XSS相比非持久性XSS攻击危害性更大,容易造成蠕虫,因为每当用户打开页面,查看内容时脚本将自动执行。

该网页有一个发表评论的功能,该评论会写入后台数据库,并且访问主页的时候,会从数据库中加载出所有的评论。

XSS:  通过客户端脚本语言 (最常见如: JavaScript)

在一个论坛发帖中发布一段恶意的JavaScript代码就是脚本注入,如果这个代码内容有请求外部服务器,那么就叫做XSS！

### XSS 的危害有多大

恶意脚本能造成多大危害，关键在于它是**以网站自身的身份**在浏览器里执行的，而不是像 CSRF 那样被挡在同源策略之外：

- **能读到该站的 cookie/session**（除非设了 `HttpOnly`），偷到后攻击者可以直接把这个 cookie 装进自己的浏览器，冒充受害者登录（session 劫持），完全不需要密码。
- **能以用户身份正常调用该站的接口，并读到响应内容**：这一点比 CSRF 更强——CSRF 只能"盲发"一次请求（拿不到返回结果），而 XSS 脚本运行在页面里，可以正常 `fetch`/`XMLHttpRequest`，读到余额、订单、其他敏感数据，甚至先读到页面里的 CSRF token 再拿它发起改密码请求，等于绕过了 CSRF 防护。
- **发送数据出去不受同源策略限制**：SOP 只挡"读取跨域响应"，不挡"往外发请求"。所以脚本可以用 `fetch`/`<img src>`/`navigator.sendBeacon` 把偷到的 cookie、表单输入，悄悄发到攻击者自己的服务器。
- **能篡改页面**：改 DOM、插入钓鱼表单（伪装成"重新登录"骗二次密码）、加键盘记录器、挂广告或挖矿脚本。
- **存储型可以自我传播**：经典案例是 2005 年 MySpace 的 **Samy worm**——一段存储型 XSS，只要有人访问了带毒页面，这段代码就会自动复制到访问者自己的页面里，24 小时内感染了 100 多万用户。

需要注意的是，危害范围**并非无限**，而是受限于**受害者本人的权限**：普通用户中招，脚本也只能以普通用户身份操作；如果受害者恰好是管理员，危害就是整站级别的——这也是管理后台的 XSS 漏洞格外危险的原因。

一句话对比：**CSRF 是让浏览器发送了一个不该发的请求（看不到结果、读不到 cookie）；XSS 是让浏览器执行了一段不该执行的代码（拿到了受害者在这个站点的全部会话权限，还能把偷到的东西带出去交给攻击者）**，这就是为什么 XSS 通常被认为比 CSRF 危害更全面。

### CSRF，Cross-site request forgery， 跨站请求伪造

又称 XSRF, 冒充用户发起请求 (在用户不知情的情况下) ,完成一些违背用户意愿的请求 (如恶意发帖, 删帖, 改密码, 发邮件等).
XSS 更偏向于方法论, CSRF 更偏向于一种形式, 只要是伪造用户发起的请求, 都可成为 CSRF 攻击。

通常来说 CSRF 是由XSS实现的, 所以 CSRF 时常也被称为 XSRF [用XSS的方式实现伪造请求]  (但实现的方式绝不止一种, 还可以直接通过命令行模式 (命令行敲命令来发起请求) 直接伪造请求 [只要通过合法验证即可]) 。

XSS 更偏向于代码实现 (即写一段拥有跨站请求功能的 JavaScript 脚本注入到一条帖子里, 然后有用户访问了这个帖子, 这就算是中了 XSS 攻击了), CSRF 更偏向于一个攻击结果, 只要发起了冒牌请求那么就及本质/危害辨析；新增「XSS 的危害有多大」小节（读 cookie/session、能读接口响应、出站不受同源限制、Samy worm 蠕虫案例、权限边界=受害者权限、与 CSRF 的一句话对比） | 便于与站内其他 CSRF/JWT 相关文章互相跳转；澄清读者对 XSS/CSRF 攻击本质与危害边界的常见

**CSRF 的本质：浏览器自动附带 cookie，而不是跨站读取或转发 cookie**

CSRF 常被误解为"A 站读到了 B 站的 cookie，再发给 B 站"或者"把 cookie 发给了 A 站"，两者都不对。Cookie 是按域名自动附加的，与请求由谁发起无关：当 A 站页面里的代码向 B 站发起请求时（如 `<img src="...">`、自动提交的表单），浏览器只看到"这是一个发往 B 站的请求"，于是照常把 B 站的 cookie 附加上去一起发出——A 站全程既读不到也碰不到这个 cookie，只是"制造"了这个请求，剩下的事全靠浏览器的自动行为完成。

正因如此，CSRF 造成的是货真价实的损失，不是恶作剧：请求带着真实有效的 cookie 到达 B 站，B 站服务器验证通过，认为是用户本人在操作，于是真的执行了转账、改密码、改密保邮箱等动作。这也是"confused deputy"（被混淆的代理人）这个说法的由来——浏览器被 A 站忽悠，稀里糊涂地拿着 B 站给的授权替 A 站办了事。

更完整的 CSRF 攻击案例（银行转账、论坛图片标签、多窗口浏览器会话共享等）见 [CSRF/XSRF](../web/csrfxsrf.md)；防御 CSRF 的具体 cookie 属性（`HttpOnly`/`SameSite`/`Secure`）见 [JWT vs Session：认证方式对比](../web/jwt-session.md) 的「安全性」小节。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-02 | 补充 lastmod；标签由 reprint 改为具体技术标签（xss/csrf/cors/security）+ remix + AI-assisted；在 CSRF 小节新增站内相关文章链接，并补充「CSRF 本质是浏览器自动附带 cookie、而非跨站读取转发」及「CSRF 会造成真实损失」的辨析 | 便于与站内其他 CSRF/JWT 相关文章互相跳转；澄清读者常见的两个误解 |

