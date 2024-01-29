---
title: java exit code
author: "-"
date: 2015-12-30T07:25:26+00:00
url: /?p=8612
categories:
  - Inbox
tags:
  - reprint
---
## java exit code

  http://blog.sina.com.cn/s/blog_5396eb53010004sg.html


  The number is only the status code for the termination of the JVM. It does not effect the actual command. By convention 0 means a normal exit, anything else signifies an abnormal termination.


  
    You can actually return any int not just a 1 or 0. A common searching for was found, Exit 1 means that the text you were searching for was not found and Exit 2 means it barfed. 
    
    
      To get a handle no the exit status, the env variable "$?" is the return status of the last command. So try this:
    
    
    
      bash$ cat "SOME_FILE_THAT_DOES_NOT_EXIST"
 bash$ echo $?
 and your result should be 1.
    
    
    
      bash$ cat "SOME_FILE_THAT_DOES_EXIST"
 bash$ echo $?
 and your result should be 0.
    
    
    
      hope this helps,
 cludwin
  
