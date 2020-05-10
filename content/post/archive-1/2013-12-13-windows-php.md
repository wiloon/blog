---
title: windows php
author: wiloon
type: post
date: 2013-12-13T06:23:42+00:00
url: /?p=6036
categories:
  - Uncategorized

---
<div>
  <p>
    apache软件no_ssl和openssl两种类型的区别
  </p>
</div>

<div id="content">
  <p>
    apache软件同一版本有两种类型：no_ssl和openssl:
  </p>
  
  <p>
    openssl多了个ssl安全认证模式，它的协议是HTTPS而不是HTTP，这就是带有SSL的服务器与一般网页服务器的区别了。
  </p>
  
  <p>
    一般情况下，我们下载no_ssl版本的就ok了。
  </p>
  
  <h3>
    Apache HTTP 服务器
  </h3>
  
  <ol>
    <li>
      下载 <a href="http://httpd.apache.org/download.cgi" target="_blank">Apache2 HTTP 服务器</a>。
    </li>
    <li>
      运行安装文件 <tt>.msi</tt>。此时将启动安装向导。按照说明操作。在 Microsoft Vista 上，不要将 Apache 服务器安装到 Program Files 中的默认位置。Program Files 中的所有文件均具有写保护。
    </li>
    <li>
      安装完成后，重新启动 Apache 服务器。
    </li>
    <li>
      要检查安装是否成功，请运行浏览器，然后输入以下 URL： <pre>  http://localhost/</pre>
      
      <p>
        Apache 欢迎测试页面打开：</li> </ol> 
        
        <h4>
          疑难解答
        </h4>
        
        <p>
          默认情况下，Apache 服务器监听端口 80。此端口可能已被其他服务所使用，如 Skype。要解决此问题，请更改服务器监听的端口：
        </p>
        
        <ol>
          <li>
            打开 Apache Web 服务器配置文件 <tt>httpd.conf</tt>。默认情况下，此文件位于 <tt>C:\Program Files\Apache Software Foundation\Apache<version>\conf\</tt> 中
          </li>
          <li>
            找到 <tt>Listen 80</tt> 行，并更改端口号，如 <tt>8080</tt>。保存该文件。
          </li>
          <li>
            重新启动 Apache Web 服务器。
          </li>
          <li>
            要检查 Web 服务器是否工作，请运行浏览器并输入 URL，然后明确指定端口号：<tt>http://localhost:8080</tt>
          </li>
        </ol>
        
        <p>
          您还可以停止可能监听端口 80 的进程。在任务管理器中，选择相关文件名称，并单击“结束进程”。
        </p>
        
        <p>
          <a href="http://blog.csdn.net/maxracer/article/details/7298737">http://blog.csdn.net/maxracer/article/details/7298737</a>
        </p>
        
        <p>
          <a href="https://netbeans.org/kb/docs/php/configure-php-environment-windows_zh_CN.html">https://netbeans.org/kb/docs/php/configure-php-environment-windows_zh_CN.html</a>
        </p></div>