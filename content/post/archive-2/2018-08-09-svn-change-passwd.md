---
title: svn change passwd
author: "-"
type: post
date: 2018-08-09T06:27:13+00:00
url: /?p=12505
categories:
  - Uncategorized

---
svn change password
  
1. after svn password changed, delete the folder $HOME/.subversion
  
2. run svn checkout -username user svn://server/repo, input new password
  
3. run git svn