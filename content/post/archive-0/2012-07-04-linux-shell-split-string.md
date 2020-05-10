---
title: linux shell split string
author: wiloon
type: post
date: 2012-07-04T09:03:48+00:00
url: /?p=3728
categories:
  - Linux

---
[shell]
  
sentence="This is   a sentence."
  
for word in $sentence
  
do
  
echo $word
  
done
  
[/shell]

``

[shell]This
  
is
  
a
  
sentence.
  
[/shell]