---
title: linux sha1sum
author: "-"
date: 2014-03-22T05:50:14+00:00
url: /?p=6438
categories:
  - Inbox
tags:
  - Linux

---
## linux sha1sum
> Print or check SHA1 (160-bit) checksums. With no FILE, or when FILE is -, read standard input.

    sha1sum {file}
    

If you want to send the file together with its sha1sum output redirect the output to a file:

    sha1sum {file} > {file}.sha1
    

Send both files and the other party can do a...

    sha1sum -c {file}.sha1
    

It should show `OK` if the `sha1` is correct.