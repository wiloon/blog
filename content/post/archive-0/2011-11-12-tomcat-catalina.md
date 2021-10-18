---
title: 'Tomcat & Catalina'
author: "-"
type: post
date: 2011-11-12T07:07:16+00:00
url: /?p=1498
bot_views:
  - 10
views:
  - 7
categories:
  - Java
tags:
  - Tomcat

---
# 'Tomcat & Catalina'
catalina   是   tomcat   4.x   的   servlet   container，起源是加州的一个岛名，本身和猫没有什么关系，所以   tomcat:catalina   的类比一定不能选   apple:macintosh（macintosh   是美国的一种苹果，个头甚大) 。但另外一方面，PBY   catalina   是一种远程轰炸机，而   apache   是   Jane 's   鼎鼎大名的直升机，所以   catalina:apache   和   apple:macintosh   勉强有一对。

Catalina是太平洋中靠近洛杉矶的一个小岛。因为其风景秀丽而著名。最近曾被评为全美最漂亮的小岛。

Tomcat is actually composed of a number of components, including a [Tomcat JSP][1] engine and a variety of different connectors, but its core component is called Catalina.  Catalina provides Tomcat's actual implementation of the servlet specification; when you [start up your Tomcat server][2], you're actually starting Catalina.

In this article, we'll get to know Tomcat's core component, from the [origins of the name "Catalina"][3], to an overview of [how Catalina is configured][4].  We'll also look at some Catalina-related tips and tricks, such as how to get the most out of [Catalina's built-in logging][5] functionality, and how to [manage the Catalina class as an MBean][6] using JMX.

  Tired of wading through hundreds of lines of XML just to make a simple change to your Tomcat configuration?  Tcat makes Tomcat configuration simple.  Create optimized configuration profiles, save them, and apply them to groups of servers with a single click.

## How Did Catalina Get Its Name?

There's nothing like an Apache product name to raise an eyebrow - the Apache volunteers have a knack for turning out oddly named technologies that's only rivaled by Ubuntu's "adjective-animal" naming format.

The name "Catalina," according to Craig McClanahan, who designed the original architecture of the servlet container, can be attributed to three things: his love for Catalina Island (despite never having visited it), his cat's habit of hanging around the computer while he was writing the code, and the consideration, at an early stage of development, of building Tomcat on a server framework called Avalon, which is the name of a town on Catalina island.

The Avalon framework was eventually abandoned, but the name stuck, and the rest is history.

<http://www.mulesoft.com/tomcat-catalina>

 [1]: http://www.mulesoft.com/tomcat-jsp
 [2]: http://www.mulesoft.com/tomcat-start
 [3]: http://www.mulesoft.com/tomcat-catalina#name
 [4]: http://www.mulesoft.com/tomcat-catalina#config
 [5]: http://www.mulesoft.com/tomcat-catalina#logging
 [6]: http://www.mulesoft.com/tomcat-catalina#mbean