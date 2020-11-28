---
title: html radio button
author: w1100n
type: post
date: 2011-08-08T03:41:01+00:00
url: /?p=409
bot_views:
  - 8
views:
  - 1
categories:
  - Uncategorized

---
set objElement = objPage.WebElement("html tag:=TD","innertext:=xxxxxx", "index:=1").object
  
logger(objElement.outerHtml)
  
Set objElement = objElement.parentElement
  
logger(objElement.outerHtml)
  
Set objElement = objElement.firstChild
  
logger(objElement.outerHtml)
  
Set objElement = objElement.firstChild
  
logger(objElement.outerHtml)
  
logger(objElement.status)
  
objElement.checked=true
  
logger(objElement.status)