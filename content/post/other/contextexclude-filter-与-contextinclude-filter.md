---
title: context,exclude-filter 与 context,include-filter
author: "-"
date: 2012-12-17T14:30:18+00:00
url: /?p=4919
categories:
  - Java
  - Web

tags:
  - reprint
---
## context,exclude-filter 与 context,include-filter

**1 在主容器中 (applicationContext.xml) ，将Controller的注解打消掉**

```xml

<context:component-scan base-package="com">
   
<context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller" />
  
</context:component-scan>

```

**2 而在springMVC配置文件中将Service注解给去掉**

```xml

<context:component-scan base-package="com">
   
<context:include-filter type="annotation" expression="org.springframework.stereotype.Controller" />
   
<context:exclude-filter type="annotation" expression="org.springframework.stereotype.Service" />
   
</context:component-scan>

```

**因为spring的context是父子容器，所以会产生冲突，Controller会进步前辈行扫描装配，而此时的Service还没有进行事务的加强处理，获得的将是原样的Service (没有经过事务加强处理，故而没有事务处理能力)  ，最后才是applicationContext.xml中的扫描设备进行事务处理**