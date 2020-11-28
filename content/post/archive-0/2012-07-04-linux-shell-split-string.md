---
title: linux shell split string
author: w1100n
type: post
date: 2012-07-04T09:03:48+00:00
url: /?p=3728
categories:
  - Linux

---
```bash
  
sentence="This is   a sentence."
  
for word in $sentence
  
do
  
echo $word
  
done
  
```

``

```bashThis
  
is
  
a
  
sentence.
  
```