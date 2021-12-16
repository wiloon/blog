---
title: emacs在替换字符串的时候输入回车/换行
author: "-"
date: 2011-12-01T07:38:21+00:00
url: /?p=1660
categories:
  - Emacs

---
## emacs在替换字符串的时候输入回车/换行
`C-Q C-J`

**Using carriage returns in query-replace / replace-string**


  
    Use C-Q C-J (control-Q control-J) each time you want to include a carriage return. e.g. to double-space everything
  
  
    M-x replace-string RET C-Q C-J RET C-Q C-J C-Q C-J RET
  
  
    Or to put "bloogie " at the beginning of every line
  
  
    M-x replace-string RET C-Q C-J RET C-Q C-J b l o o g i e SPACE RET
  
