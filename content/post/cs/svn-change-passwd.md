---
title: svn change passwd
author: "-"
date: 2018-08-09T06:27:13+00:00
url: /?p=12505
categories:
  - Inbox
tags:
  - reprint
---
## svn change passwd
svn change password
  
1. after svn password changed, delete the folder $HOME/.subversion
  
2. run svn checkout -username user svn://server/repo, input new password
  
3. run git svn