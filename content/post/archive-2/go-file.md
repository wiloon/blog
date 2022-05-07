---
title: go file
author: "-"
date: 2017-10-31T03:11:46+00:00
url: /?p=11343
categories:
  - Inbox
tags:
  - reprint
---
## go file
os.PathSeparator

file, _ := os.Getwd()
              
log.Println("current path:", file)

            file, _ = exec.LookPath(os.Args[0])
            log.Println("exec path:", file)
    
            dir,_ := path.Split(file)
            log.Println("exec folder relative path:", dir)
    
            os.Chdir(dir)
            wd, _ := os.Getwd()
            log.Println("exec folder absolute path:", wd)