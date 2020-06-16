---
title: 'Debian – Apt-get : NO_PUBKEY / GPG error'
author: wiloon
type: post
date: 2011-12-17T05:54:56+00:00
url: /?p=1912
categories:
  - Linux

---
The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 010908312D230C5F

## Solution



    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3C962022012520A0
    

Simply type the following commands, taking care to replace the number of the key that displayed in the error message:
  
gpg &#8211;keyserver pgpkeys.mit.edu &#8211;recv-key 010908312D230C5F
  
gpg -a &#8211;export 010908312D230C5F | sudo apt-key add &#8211;