---
title: spring mvc annotation
author: w1100n
type: post
date: 2014-05-07T11:25:46+00:00
url: /?p=6603
categories:
  - Uncategorized
tags:
  - SpringMVC

---
  * 参数处理（明确指定参数 匹配 自动转换类型） 
    >>普通属性和对象及属性: @RequestParam("id")注解，所以它将和id的URL参数绑定</li> 
    
      * 
      * **@RequestBody** 将HTTP请求正文转换为适合的HttpMessageConverter对象。
      * **@ResponseBody** 将内容或对象作为 HTTP 响应正文返回，并调用适合HttpMessageConverter的Adapter转换对象，写入输出流。
      * @PathVariable</ul> 
    
    <span style="color: #000000;">@PathVariable是用来对指定请求的URL路径里面的变量 <br style="color: #000000;" /><span style="color: #000000;">eg: 
    
    <div id="" class="dp-highlighter" style="color: #000000;">
      <div class="bar">
        <div class="tools" style="font-weight: bold;">
          Java代码  <a style="color: #108ac6;" title="收藏这段代码"><img class="star" src="http://yeak2001.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
        
      
      
      <ol class="dp-j" style="color: #2b91af;" start="1">
        <li>
          <span style="color: black;"><span class="annotation" style="color: #646464;">@RequestMapping(value = <span class="string" style="color: blue;">"form/{id}/apply", method = {RequestMethod.PUT, RequestMethod.POST})  
        </li>
      </ol>
    
    
    <br style="color: #000000;" /><br style="color: #000000;" /><span style="color: #000000;">{id}在这个请求的URL里就是个变量，可以使用@PathVariable来获取 <br style="color: #000000;" /><span style="color: #000000;">@PathVariable和@RequestParam的区别就在于: @RequestParam用来获得静态的URL请求入参
    
    
    
    ### 、 @PathVariable <wbr />
    
    当使用@RequestMapping URI template 样式映射时， 即 someUrl/{paramId}, 这时的paramId可通过 @Pathvariable注解绑定它传过来的值到方法的参数上。
    
    示例代码: 
    
    <wbr />
    
    
      
        <div style="color: silver;">
          
            ```java```
          
          
          
http://blog.csdn.net/walkerjong/article/details/7946109#
          
          
          
          
        
      
      
      <ol style="color: #5c5c5c;" start="1">
        <li style="color: inherit;">
          <span style="color: black;"><span style="color: #646464;">@Controller <wbr /> <wbr />
        </li>
        <li>
          <span style="color: black;"><span style="color: #646464;">@RequestMapping(<span style="color: blue;">"/owners/{ownerId}") <wbr /> <wbr />
        </li>
        <li style="color: inherit;">
          <span style="color: black;"><span style="font-weight: bold; color: #006699;">public <wbr /><span style="font-weight: bold; color: #006699;">class <wbr />RelativePathUriTemplateC<wbr />ontroller <wbr />{ <wbr /> <wbr />
        </li>
        <li>
          <span style="color: black;"> <wbr /> <wbr />
        </li>
        <li style="color: inherit;">
          <span style="color: black;"> <wbr /> <wbr /><span style="color: #646464;">@RequestMapping(<span style="color: blue;">"/pets/{petId}") <wbr /> <wbr />
        </li>
        <li>
          <span style="color: black;"> <wbr /> <wbr /><span style="font-weight: bold; color: #006699;">public <wbr /><span style="font-weight: bold; color: #006699;">void <wbr />findPet(<span style="color: #646464;">@PathVariable <wbr />String <wbr />ownerId, <wbr /><span style="color: #646464;">@PathVariable <wbr />String <wbr />petId, <wbr />Model <wbr />model) <wbr />{ <wbr /> <wbr /> <wbr /> <wbr /> <wbr /> <wbr />
        </li>
        <li style="color: inherit;">
          <span style="color: black;"> <wbr /> <wbr /> <wbr /> <wbr /><span style="color: #008200;">// <wbr />implementation <wbr />omitted <wbr /> <wbr />
        </li>
        <li>
          <span style="color: black;"> <wbr /> <wbr />} <wbr /> <wbr />
        </li>
        <li style="color: inherit;">
          <span style="color: black;">} <wbr /> <wbr />
        </li>
      </ol>
    
    
    上面代码把URI template 中变量 ownerId的值和petId的值，绑定到方法的参数上。若方法参数名称和需要绑定的uri template中变量名称不一致，需要在@PathVariable("name")指定uri template中的名称。
    
    http://blog.csdn.net/zshake/article/details/9716849
    
    http://yeak2001.iteye.com/blog/465336
    
    http://blog.sina.com.cn/s/blog_72827fb10101pl9j.html