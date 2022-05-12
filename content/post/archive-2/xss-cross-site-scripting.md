---
title: XSS, Cross Site Scripting, CSRF, Cross-site request forgery, CORS
author: "-"
date: 2018-12-13T06:38:16.000+00:00
url: XSS
categories:
- Web
tags:
  - reprint
---
## XSS, Cross Site Scripting, CSRF, Cross-site request forgery, CORS
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

### CSRF，Cross-site request forgery， 跨站请求伪造

又称 XSRF, 冒充用户发起请求 (在用户不知情的情况下) ,完成一些违背用户意愿的请求 (如恶意发帖, 删帖, 改密码, 发邮件等). 
XSS 更偏向于方法论, CSRF 更偏向于一种形式, 只要是伪造用户发起的请求, 都可成为 CSRF 攻击。

通常来说 CSRF 是由XSS实现的, 所以 CSRF 时常也被称为 XSRF [用XSS的方式实现伪造请求]  (但实现的方式绝不止一种, 还可以直接通过命令行模式 (命令行敲命令来发起请求) 直接伪造请求 [只要通过合法验证即可]) 。

XSS 更偏向于代码实现 (即写一段拥有跨站请求功能的 JavaScript 脚本注入到一条帖子里, 然后有用户访问了这个帖子, 这就算是中了 XSS 攻击了), CSRF 更偏向于一个攻击结果, 只要发起了冒牌请求那么就算是 CSRF 了。

### CORS， Cross-Origin Resource Sharing, 跨源资源共享, 跨域资源共享
由于现实使用中，很多需要跨域访问，所以 W3C 标准就提出了 CORS。

跨域资源共享(CORS) 是一种机制，它使用额外的 HTTP 头来告诉浏览器 让运行在一个 origin (domain) 上的Web应用被准许访问来自不同源服务器上的指定的资源。当一个资源从与该资源本身所在的服务器不同的域、协议或端口请求一个资源时，资源会发起一个跨域 HTTP 请求。

具体查看官方文档：https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS
https://tech.meituan.com/2018/09/27/fe-security.html
简单里的理解，就是 CORS 提供了一种设置你的页面可以访问指定的域名下的资源 (API）的方法。当然这些域名是你受信任的。从而避免了 CRSF 攻击。CORS 就像是一个过滤器。

注意：很多开发者在碰到跨域问题提时，通过搜索得到的答案就是直接设置 Oragin: * 这样的结果就是你的网页信任任何域名，虽然达到了跨域访问的目的，但是同时失去了 CORS 的意义，因为你设置了这个过滤器不过滤任何域

>https://www.ruanyifeng.com/blog/2016/04/cors.html
>https://tech.meituan.com/2018/09/27/fe-security.html
https://github.com/OWASP?page=5

https://github.com/owasp/java-html-sanitizer

https://www.owasp.org/index.php/Category:OWASP_AntiSamy_Project

https://mvnrepository.com/artifact/org.owasp.antisamy/antisamy

https://github.com/GDSSecurity/AntiXSS-for-Java

https://segmentfault.com/a/1190000007059639

https://www.freebuf.com/sectool/134015.html

https://blog.csdn.net/ru_li/article/details/51334082

https://blog.csdn.net/zer0_o/article/details/28399533


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

###
#### Access-Control-Allow-Origin

该字段是必须的。它的值要么是请求时Origin字段的值，要么是一个*，表示接受任意域名的请求。

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


>https://www.ruanyifeng.com/blog/2016/04/cors.html
