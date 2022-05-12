---
title: cxf wsdl2java
author: "-"
date: 2012-07-06T01:44:43+00:00
url: /?p=3755
categories:
  - Java
  - Web
tags:$
  - reprint
---
## cxf wsdl2java
```bash
  
wsdl2java -d src -client http://localhost:9000/helloWorld?wsdl
  
```

其作用上面的build.xml作用一样。
  
附加: wsdl2java用法: 
  
wsdl2java -p com -d src -all  aa.wsdl
  
-p  指定其wsdl的命名空间，也就是要生成代码的包名:
  
-d  指定要产生代码所在目录
  
-client 生成客户端测试web service的代码
  
-server 生成服务器启动web  service的代码
  
-impl 生成web service的实现代码
  
-ant  生成build.xml文件
  
-all 生成所有开始端点代码: types,service proxy,,service interface, server mainline, client mainline, implementation object, and an Ant build.xml file.
  
详细用法见: http://cwiki.apache.org/CXF20DOC/wsdl-to-java.html