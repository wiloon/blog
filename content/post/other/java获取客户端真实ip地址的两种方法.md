---
title: Java获取客户端真实IP地址的两种方法
author: "-"
date: 2014-03-13T06:53:05+00:00
url: /?p=6399
categories:
  - Uncategorized
tags:
  - Java

---
## Java获取客户端真实IP地址的两种方法
http://dpn525.iteye.com/blog/1132318

在JSP里，获取客户端的IP地址的方法是: request.getRemoteAddr () ，这种方法在大部分情况下都是有效的。但是在通过了Apache，Squid等反向代理软件就不能获取到客户端的真实IP地址了。

在JSP里，获取客户端的IP地址的方法是: request.getRemoteAddr () ，这种方法在大部分情况下都是有效的。但是在通过了Apache，Squid等反向代理软件就不能获取到客户端的真实IP地址了。

如果使用了反向代理软件，将http://192.168.1.110: 2046/ 的URL反向代理为 http://www.javapeixun.com.cn / 的URL时，用request.getRemoteAddr () 方法获取的IP地址是: 127.0.0.1或192.168.1.110，而并不是客户端的真实IP。

经过代理以后，由于在客户端和服务之间增加了中间层，因此服务器无法直接拿到客户端的IP，服务器端应用也无法直接通过转发请求的地址返回给客户端。但是在转发请求的HTTP头信息中，增加了X－FORWARDED－FOR信息。用以跟踪原有的客户端IP地址和原来客户端请求的服务器地址。当我们访问http://www.javapeixun.com.cn/index.jsp/ 时，其实并不是我们浏览器真正访问到了服务器上的index.jsp文件，而是先由代理服务器去访问http://192.168.1.110: 2046/index.jsp ，代理服务器再将访问到的结果返回给我们的浏览器，因为是代理服务器去访问index.jsp的，所以index.jsp中通过request.getRemoteAddr () 的方法获取的IP实际上是代理服务器的地址，并不是客户端的IP地址。

于是可得出获得客户端真实IP地址的方法一: 

Java代码 收藏代码

public String getRemortIP(HttpServletRequest request) {

if (request.getHeader("x-forwarded-for") == null) {

return request.getRemoteAddr();

}

return request.getHeader("x-forwarded-for");

}

可是当我访问http://www.5a520.cn /index.jsp/ 时，返回的IP地址始终是unknown，也并不是如上所示的127.0.0.1或192.168.1.110了，而我访问http://192.168.1.110: 2046/index.jsp 时，则能返回客户端的真实IP地址，写了个方法去验证。原因出在了Squid上。squid.conf 的配制文件forwarded_for 项默认是为on，如果 forwarded_for 设成了 off 则: X-Forwarded-For:  unknown

于是可得出获得客户端真实IP地址的方法二: 

Java代码 收藏代码

public String getIpAddr(HttpServletRequest request) {

String ip = request.getHeader("x-forwarded-for");

if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {

ip = request.getHeader("Proxy-Client-IP");

}

if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {

ip = request.getHeader("WL-Proxy-Client-IP");

}

if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {

ip = request.getRemoteAddr();

}

return ip;

}

可是，如果通过了多级反向代理的话，X-Forwarded-For的值并不止一个，而是一串IP值，究竟哪个才是真正的用户端的真实IP呢？

答案是取X-Forwarded-For中第一个非unknown的有效IP字符串。

如: X-Forwarded-For: 192.168.1.110， 192.168.1.120， 192.168.1.130， 192.168.1.100用户真实IP为:  192.168.1.110


-------

http://www.oschina.net/question/819166_124476

一般的话，在 Servlet 中会先从 HTTP 请求头中获取，这是因为 Servlet 容器并不一定是真正暴露在 Internet 上的，而是通过 Web 服务器，甚至是负载均衡设备之后的，一个客户端的请求过来，经过了好几次的反向代理，如果直接使用 HttpServletRequest 的 getRemoteAddr() 获取的将是位于 Servlet 上一层代理服务器的 IP 地址，因此这种方式在生产环境中是不可靠的。


一般通过反向代理服务器的客户端请求，代理服务器都会将客户端源 IP 地址附加在原始的 HTTP 请求头上，非标准协议的代理源 IP 地址请求头有 X-Forwarded-For、X-Real-Ip 等，可以直接依据优先级从这些 HTTP 头获取数据，如果实现在获取不到的话，再从 HttpServletRequest 的 getRemoteAddr() 方法中获取。


参考代码如下: 


Java代码 收藏代码

/**

* 

* Web 服务器反向代理中用于存放客户端原始 IP 地址的 Http header 名字，

* 若新增其他的需要增加或者修改其中的值。

* 

*/

private static final String[] PROXY_REMOTE_IP_ADDRESS = { "X-Forwarded-For", "X-Real-IP" };

/**

* 

* 获取请求的客户端的 IP 地址。若应用服务器前端配有反向代理的 Web 服务器，

* 需要在 Web 服务器中将客户端原始请求的 IP 地址加入到 HTTP header 中。

* 详见 {@link #PROXY_REMOTE_IP_ADDRESS}

* 

*/

public static String getRemoteIp( HttpServletRequest request ) {

for ( int i = 0 ; i < PROXY_REMOTE_IP_ADDRESS.length ; i++ ) {

String ip = request.getHeader( PROXY_REMOTE_IP_ADDRESS[i] );

if ( ip != null && ip.trim().length > 0 ) {

return getRemoteIpFromForward( ip.trim() );

}

}

return request.getRemoteHost();

}


/**

* 

* 从 HTTP Header 中截取客户端连接 IP 地址。如果经过多次反向代理，

* 在请求头中获得的是以",<SP>"分隔 IP 地址链，第一段为客户端 IP 地址。

* 

*

* @param xforwardIp 从 HTTP 请求头中获取转发过来的 IP 地址链

* @return 客户端源 IP 地址

*/

private static String getRemoteIpFromForward( String xforwardIp ) {

int commaOffset = xforwardIp.indexOf( ',' );

if ( commaOffset < 0 ) {

return xforwardIp;

}

return xforwardIp.substring( 0 , commaOffset );

}