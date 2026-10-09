---
title: spring @value
author: "-"
date: 2014-11-07T02:44:15+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: spring-value
categories:
  - Java
tags:
  - Spring
  - remix
  - AI-assisted
aliases:
  - /p7004/
---
## spring @value

在spring 3.0中,可以通过使用@value,对一些如xxx.properties文件
  
中的文件,进行键值对的注入,例子如下:

1 首先在applicationContext.xml中加入:
  
```xml
<beans xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util-3.1.xsd">
</beans>
```

的命名空间,然后

```xml
<util:properties id="settings" location="WEB-INF/classes/META-INF/spring/test.properties" />
```

3 创建test.properties
  
abc=123

import org.springframework.beans.factory.annotation.Value;
  
import org.springframework.stereotype.Controller;
  
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/admin/images")
  
@Controller
  
public class ImageAdminController {

private String imageDir;
  
@Value("#{settings['test.abc']}")
  
public void setImageDir(String val) {
  
this.imageDir = val;
  
}

}
  
这样就将test.abc的值注入了imageDir中了

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Java | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
