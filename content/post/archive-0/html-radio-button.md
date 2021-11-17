---
title: html radio button
author: "-"
date: 2011-08-08T03:41:01+00:00
url: /?p=409
views:
  - 1
categories:
  - Uncategorized

---
## html radio button
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