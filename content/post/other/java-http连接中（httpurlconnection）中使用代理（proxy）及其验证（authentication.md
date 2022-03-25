---
title: Java Http连接中 (HttpURLConnection) 中使用代理 (Proxy) 及其验证 (Authentication) 
author: "-"
date: 2012-09-27T02:11:49+00:00
url: /?p=4338
categories:
  - Java

tags:
  - reprint
---
## Java Http连接中 (HttpURLConnection) 中使用代理 (Proxy) 及其验证 (Authentication)
```java

System.setProperty("http.proxyHost", "www.proxy.com");
  
System.setProperty("http.proxyPort", "8080");

```

使用Java的HttpURLConnection类可以实现HttpClient的功能，而不需要依赖任何其他类库。所有有时候大家就直接使用它来完成一些简单 (或复杂) 的功能。但是你活在伟大的{print G.F.W}后面，如果你需要访问的网站被墙了，那HttpURLConnection类就会出现连接超时的错误。这时候就需要给他设置代理 (Proxy) 了。


  
          设置代理 (Proxy) 可以有两种方式: 
  
  
    1、通过设置系统属性(System.setPropery(String key, String value)的方式
  
  
    首先你可以在这里看到Java支持的属性。我们可以使用其中的http.proxyHost，http.proxyPort这两个属性。顾名思义，就是分别设置代理服务器地址和代理端口。
  
  
    
      [c language="-sharp"][/c]
  
  
  
  
    替换上面的www.proxy.com为你的代理服务器地址或IP地址，以及相应的端口为真实端口，Http连接及可以工作了。需要注意的是如果你设置了这些属性，那么所有的Http请求都会通过代理服务器。这些属性是JVM级别的，设置了以后对所有的同类请求都有效。比如上面的是关于http的，还有关于ftp的等等。
  
  
    如果你的代理服务器不需要验证，那到此就结束了。但一般都是需要验证的。但是你要是看了上面Java支持的属性列表，你就会发现那里面并没有期望中的
  
  
    
      
        
          [c language="-sharp"][/c]
        
        
        
http://blog.csdn.net/redhat456/article/details/6149774#
        
        
        
        
      
    
    
    
      
        http.proxyUserName=username
      
      
        http.proxyPassword=password
      
    
  
  
    这两个属性。 这时就需要java.net.Authenticator类来完成一般的Http验证。但是java.net.Authenticator这个类却是个抽象类，我们要使用还需要实例化一下子自己的类。个人觉得这里很不方便。如下: 
  
  
    
      
        
          ```java```
        
        
        
http://blog.csdn.net/redhat456/article/details/6149774#
        
        
        
        
      
    
  
        
        
http://blog.csdn.net/redhat456/article/details/6149774#
        
        
        
        
      
    
    
    
      
        Authenticator.setDefault(new BasicAuthenticator(userName, password));
      
    
  
  
  
  
    这样就提供了基于Http Basic的验证，接着就可以顺畅的使用需要验证的代理了。
  
  
    2、通过java.net.Proxy类。
  
  
    这种方式是实例化一个Proxy类提供代理服务器的信息，如端口和地址。
  
  
    
      
        
          ```java```
        
        
        
http://blog.csdn.net/redhat456/article/details/6149774#
        
        
        
        
      
    
    
    
      
        Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(host, port));
      
      
        URLConnection conn = url.openConnection(proxy);
      
    
  
  
  
  
    使用代理的方式是在打开Http连接的时候同时传递一个Proxy参数。如果需要验证信息的话我们可以添加一个Http头参数来实现。
  
  
    
      
        
          ```java```
        
        
        
http://blog.csdn.net/redhat456/article/details/6149774#
        
        
        
        
      
    
    
    
      
        //格式如下: 
      
      
        "Proxy-Authorization"= "Basic Base64.encode(user:password)"
      
      
        String headerKey = "Proxy-Authorization";
      
      
        String headerValue = "Basic " + Base64.encode(user+":"+password);
      
      
        conn.setRequestProperty(headerKey, headerValue);
      
      
      
      
        //..........
      
    
  
  
  
  
    其中的Base64.encode(user:password)是指把用户名和密码用冒号连接起来之后使用Base64编码后的值作为值的一部分。
  
  
    通过这种方式只影响特定的Http连接，但是需要对代码进行修改。这种方式下是否可以使用Authenticator还未做验证。
  
