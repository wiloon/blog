---
title: Java Http连接中（HttpURLConnection）中使用代理（Proxy）及其验证（Authentication）
author: wiloon
type: post
date: 2012-09-27T02:11:49+00:00
url: /?p=4338
categories:
  - Java

---
[java]

System.setProperty("http.proxyHost", "www.proxy.com");
  
System.setProperty("http.proxyPort", "8080");

[/java]

使用Java的HttpURLConnection类可以实现HttpClient的功能，而不需要依赖任何其他类库。所有有时候大家就直接使用它来完成一些简单（或复杂）的功能。但是你活在伟大的{print G.F.W}后面，如果你需要访问的网站被墙了，那HttpURLConnection类就会出现连接超时的错误。这时候就需要给他设置代理（Proxy）了。

<div id="article_content">
  <p>
          设置代理（Proxy）可以有两种方式：
  </p>
  
  <p>
    1、通过设置系统属性(System.setPropery(String key, String value)的方式
  </p>
  
  <p>
    首先你可以在这里看到<a href="http://download.oracle.com/javase/7/docs/api/java/net/doc-files/net-properties.html">Java支持的属性</a>。我们可以使用其中的http.proxyHost，http.proxyPort这两个属性。顾名思义，就是分别设置代理服务器地址和代理端口。
  </p>
  
  <div>
    <p>
      [c language=&#8221;-sharp&#8221;][/c]
    </p>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    替换上面的<a href="http://www.proxy.com/">www.proxy.com</a>为你的代理服务器地址或IP地址，以及相应的端口为真实端口，Http连接及可以工作了。需要注意的是如果你设置了这些属性，那么所有的Http请求都会通过代理服务器。这些属性是JVM级别的，设置了以后对所有的同类请求都有效。比如上面的是关于http的，还有关于ftp的等等。
  </p>
  
  <p>
    如果你的代理服务器不需要验证，那到此就结束了。但一般都是需要验证的。但是你要是看了上面<a href="http://download.oracle.com/javase/7/docs/api/java/net/doc-files/net-properties.html">Java支持的属性列表</a>，你就会发现那里面并没有期望中的
  </p>
  
  <div>
    <div>
      <div>
        <p>
          [c language=&#8221;-sharp&#8221;][/c]
        </p>
        
        <p>
          <a title="view plain" href="http://blog.csdn.net/redhat456/article/details/6149774#">view plain</a><a title="copy" href="http://blog.csdn.net/redhat456/article/details/6149774#">copy</a><a title="print" href="http://blog.csdn.net/redhat456/article/details/6149774#">print</a><a title="?" href="http://blog.csdn.net/redhat456/article/details/6149774#">?</a>
        </p>
        
        <div>
        </div>
      </div>
    </div>
    
    <ol start="1">
      <li>
        http.proxyUserName=username
      </li>
      <li>
        http.proxyPassword=password
      </li>
    </ol>
  </div>
  
  <p>
    这两个属性。 这时就需要java.net.Authenticator类来完成一般的Http验证。但是java.net.Authenticator这个类却是个抽象类，我们要使用还需要实例化一下子自己的类。个人觉得这里很不方便。如下：
  </p>
  
  <div>
    <div>
      <div>
        <p>
          [java][/java]
        </p>
        
        <p>
          <a title="view plain" href="http://blog.csdn.net/redhat456/article/details/6149774#">view plain</a><a title="copy" href="http://blog.csdn.net/redhat456/article/details/6149774#">copy</a><a title="print" href="http://blog.csdn.net/redhat456/article/details/6149774#">print</a><a title="?" href="http://blog.csdn.net/redhat456/article/details/6149774#">?</a>
        </p>
        
        <div>
        </div>
      </div>
    </div>
    
    <ol start="1">
      <li>
        public class BasicAuthenticator extends Authenticator {
      </li>
      <li>
            String userName;
      </li>
      <li>
            String password;
      </li>
      <li>
      </li>
      <li>
            public BasicAuthenticator(String userName, String password) {
      </li>
      <li>
                this.userName = userName;
      </li>
      <li>
                this.password = password;
      </li>
      <li>
            }
      </li>
      <li>
      </li>
      <li>
            /**
      </li>
      <li>
             * Called when password authorization is needed.  Subclasses should
      </li>
      <li>
             * override the default implementation, which returns null.
      </li>
      <li>
             *
      </li>
      <li>
             * @return The PasswordAuthentication collected from the
      </li>
      <li>
             *         user, or null if none is provided.
      </li>
      <li>
             */
      </li>
      <li>
            @Override
      </li>
      <li>
            protected PasswordAuthentication getPasswordAuthentication() {
      </li>
      <li>
                return new PasswordAuthentication(userName, password.toCharArray());
      </li>
      <li>
            }
      </li>
      <li>
        }
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    我们需要覆盖java.net.Authenticator类的getPasswordAuthentication()方法，并返回一个PasswordAuthentication实例。要使他起作用，还需要设置
  </p>
  
  <div>
    <div>
      <div>
        <p>
          [java][/java]
        </p>
        
        <p>
          <a title="view plain" href="http://blog.csdn.net/redhat456/article/details/6149774#">view plain</a><a title="copy" href="http://blog.csdn.net/redhat456/article/details/6149774#">copy</a><a title="print" href="http://blog.csdn.net/redhat456/article/details/6149774#">print</a><a title="?" href="http://blog.csdn.net/redhat456/article/details/6149774#">?</a>
        </p>
        
        <div>
        </div>
      </div>
    </div>
    
    <ol start="1">
      <li>
        Authenticator.setDefault(new BasicAuthenticator(userName, password));
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    这样就提供了基于Http Basic的验证，接着就可以顺畅的使用需要验证的代理了。
  </p>
  
  <p>
    2、通过java.net.Proxy类。
  </p>
  
  <p>
    这种方式是实例化一个Proxy类提供代理服务器的信息，如端口和地址。
  </p>
  
  <div>
    <div>
      <div>
        <p>
          [java][/java]
        </p>
        
        <p>
          <a title="view plain" href="http://blog.csdn.net/redhat456/article/details/6149774#">view plain</a><a title="copy" href="http://blog.csdn.net/redhat456/article/details/6149774#">copy</a><a title="print" href="http://blog.csdn.net/redhat456/article/details/6149774#">print</a><a title="?" href="http://blog.csdn.net/redhat456/article/details/6149774#">?</a>
        </p>
        
        <div>
        </div>
      </div>
    </div>
    
    <ol start="1">
      <li>
        Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(host, port));
      </li>
      <li>
        URLConnection conn = url.openConnection(proxy);
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    使用代理的方式是在打开Http连接的时候同时传递一个Proxy参数。如果需要验证信息的话我们可以添加一个Http头参数来实现。
  </p>
  
  <div>
    <div>
      <div>
        <p>
          [java][/java]
        </p>
        
        <p>
          <a title="view plain" href="http://blog.csdn.net/redhat456/article/details/6149774#">view plain</a><a title="copy" href="http://blog.csdn.net/redhat456/article/details/6149774#">copy</a><a title="print" href="http://blog.csdn.net/redhat456/article/details/6149774#">print</a><a title="?" href="http://blog.csdn.net/redhat456/article/details/6149774#">?</a>
        </p>
        
        <div>
        </div>
      </div>
    </div>
    
    <ol start="1">
      <li>
        //格式如下：
      </li>
      <li>
        &#8220;Proxy-Authorization&#8221;= &#8220;Basic Base64.encode(user:password)&#8221;
      </li>
      <li>
        String headerKey = &#8220;Proxy-Authorization&#8221;;
      </li>
      <li>
        String headerValue = &#8220;Basic &#8221; + Base64.encode(user+&#8221;:&#8221;+password);
      </li>
      <li>
        conn.setRequestProperty(headerKey, headerValue);
      </li>
      <li>
      </li>
      <li>
        //&#8230;&#8230;&#8230;.
      </li>
    </ol>
  </div>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    其中的Base64.encode(user:password)是指把用户名和密码用冒号连接起来之后使用Base64编码后的值作为值的一部分。
  </p>
  
  <p>
    通过这种方式只影响特定的Http连接，但是需要对代码进行修改。这种方式下是否可以使用Authenticator还未做验证。
  </p>
</div>