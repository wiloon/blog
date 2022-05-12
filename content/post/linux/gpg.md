---
title: GPG
author: "-"
date: 2011-12-17T05:54:56+00:00
url: gpg
categories:
  - security
tags:$
  - reprint
---
## GPG

GNU Privacy Guard

## 'Debian – Apt-get, NO_PUBKEY / GPG error'
The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 010908312D230C5F

## Solution


    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3C962022012520A0
    

Simply type the following commands, taking care to replace the number of the key that displayed in the error message:
  
gpg -keyserver pgpkeys.mit.edu -recv-key 010908312D230C5F
  
gpg -a -export 010908312D230C5F | sudo apt-key add -