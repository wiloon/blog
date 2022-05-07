---
title: gentoo emerge install unstable version
author: "-"
date: 2015-10-01T02:16:11+00:00
url: /?p=8368
categories:
  - Inbox
tags:
  - reprint
---
## gentoo emerge install unstable version
**安装特定版本的软件**

# emerge "=python-3.2"
  
# emerge "<python-3.2"

You can also manually edit the /etc/portage/package.keywords file to unmask keyword_masked packages
  
Code:
  
echo www-client/seamonkey >> /etc/portage/package.keywords
  
If /etc/portage doesn't exist then create it
  
Code:
  
mkdir /etc/portage