---
title: spring @value
author: "-"
date: 2014-11-07T02:44:15+00:00
url: /?p=7004
categories:
  - Inbox
tags:
  - Spring

---
## spring @value
在spring 3.0中,可以通过使用@value,对一些如xxx.properties文件
  
中的文件,进行键值对的注入,例子如下: 

1 首先在applicationContext.xml中加入: 
  
<beans xmlns:util="http://www.springframework.org/schema/util"
  
xsi:schemaLocation="http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util-3.1.xsd">
  
</beans>

的命名空间,然后

<util:properties id="settings" location="WEB-INF/classes/META-INF/spring/test.properties" />

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