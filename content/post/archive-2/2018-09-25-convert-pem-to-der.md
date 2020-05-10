---
title: convert pem to der
author: wiloon
type: post
date: 2018-09-25T05:47:09+00:00
url: /?p=12695
categories:
  - Uncategorized

---
[code lang=shell]
  
openssl x509 -outform der -in certificate.pem -out certificate.der
  
[/code]