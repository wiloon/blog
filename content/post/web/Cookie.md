---
title: Cookie
author: "-"
date: 2022-01-22 16:18:16
url: Cookie
categories:
  - Web
tags:
  - reprint
---

## Cookie
### Http Cookies 中 Max-age 和 Expires 有什么区别
快速回答

Expires 为 Cookie 的删除设置一个过期的日期
Max-age 设置一个 Cookie 将要过期的秒数
IE 浏览器(ie6、ie7 和 ie8) 不支持 max-age，所有的浏览器都支持 expires
深入一些来说明

expires 参数是当年网景公司推出 Cookies 原有的一部分。在 HTTP1.1 中，expires 被弃用并且被更加易用的 max-age 所替代。你只需说明这个 Cookie 能够存活多久就可以了，而不用像之前那样指定一个日期。设置二者中的一个，Cookie 会在它过期前一直保存，如果你一个都没有设置，这个 Cookie 将会一直存在直到你关闭浏览器，这种称之为 Session Cookie。


>https://jiapan.me/2017/cookies-max-age-vs-expires/

