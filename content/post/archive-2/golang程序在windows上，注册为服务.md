---
title: golang程序在windows上,注册为服务
author: "-"
date: 2018-09-30T06:08:59+00:00
url: /?p=12719
categories:
  - Inbox
tags:
  - reprint
---
## golang 程序在windows上,注册为服务

<https://blog.csdn.net/yang8023tao/article/details/53332984>

```go
  
package main

import (
      
"log"
      
"net/http"
      
"os"

"github.com/jander/golog/logger"
      
"github.com/kardianos/service"
  
)

type program struct{}

func (p *program) Start(s service.Service) error {
      
go p.run()
      
return nil
  
}

func (p *program) run() {
      
// 代码写在这儿
  
}

func (p *program) Stop(s service.Service) error {
      
return nil
  
}

/**
   
* MAIN函数,程序入口
   
*/
  
func main() {
      
svcConfig := &service.Config{
          
Name: "", //服务显示名称
          
DisplayName: "", //服务名称
          
Description: "", //服务描述
      
}

prg := &program{}
      
s, err := service.New(prg, svcConfig)
      
if err != nil {
          
logger.Fatal(err)
      
}

if err != nil {
          
logger.Fatal(err)
      
}

if len(os.Args) > 1 {
          
if os.Args[1] == "install" {
              
s.Install()
              
logger.Println("服务安装成功")
              
return
          
}

if os.Args[1] == "remove" {
              
s.Uninstall()
              
logger.Println("服务卸载成功")
              
return
          
}
      
}

err = s.Run()
      
if err != nil {
          
logger.Error(err)
      
}
  
}
  
```

注册服务步骤

1. 运行demo/main.go 得到demo.exe文件

2. 打开cmd 切换到Demo项目目录

3. 运行输入 demo.exe install 注册服务成功

4. 注册服务成功
