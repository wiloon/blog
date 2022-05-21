---
title: spring mvc annotation
author: "-"
date: 2014-05-07T11:25:46+00:00
url: /?p=6603
categories:
  - Inbox
tags:
  - SpringMVC

---
## spring mvc annotation

* 参数处理 (明确指定参数 匹配 自动转换类型)  
    >>普通属性和对象及属性: @RequestParam("id")注解，所以它将和id的URL参数绑定

  *
  * **@RequestBody** 将HTTP请求正文转换为适合的HttpMessageConverter对象。
  * **@ResponseBody** 将内容或对象作为 HTTP 响应正文返回，并调用适合HttpMessageConverter的Adapter转换对象，写入输出流。
  * @PathVariable

    @PathVariable是用来对指定请求的URL路径里面的变量 eg:

          Java代码  <img class="star" src="http://yeak2001.iteye.com/images/icon_star.png" alt="收藏代码" />
        
      
      
      
        
          "form/{id}/apply", method = {RequestMethod.PUT, RequestMethod.POST})  

    @PathVariable和@RequestParam的区别就在于: @RequestParam用来获得静态的URL请求入参

### 、 @PathVariable

    当使用@RequestMapping URI template 样式映射时， 即 someUrl/{paramId}, 这时的paramId可通过 @Pathvariable注解绑定它传过来的值到方法的参数上。

    示例代码:

            ```java```

<http://blog.csdn.net/walkerjong/article/details/7946109>#

          @Controller  
        
        
          "/owners/{ownerId}")  
        
        
          class RelativePathUriTemplateController {  
        
        
            
        
        
          "/pets/{petId}")  
        
        
          @PathVariable String petId, Model model) {      
        
        
          // implementation omitted  
        
        
            }  
        
        
          }  
        
      
    
    
    上面代码把URI template 中变量 ownerId的值和petId的值，绑定到方法的参数上。若方法参数名称和需要绑定的uri template中变量名称不一致，需要在@PathVariable("name")指定uri template中的名称。
    
    http://blog.csdn.net/zshake/article/details/9716849
    
    http://yeak2001.iteye.com/blog/465336
    
    http://blog.sina.com.cn/s/blog_72827fb10101pl9j.html
