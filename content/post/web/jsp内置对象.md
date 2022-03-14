---
title: jsp内置对象
author: "-"
date: 2012-09-22T06:56:02+00:00
url: /?p=4173
categories:
  - Java

tags:
  - reprint
---
## jsp内置对象

  定义: 可以不加声明就在JSP页面脚本 (Java程序片和Java表达式) 中使用的成员变量


  JSP共有以下9种基本内置组件 (可与ASP的6种内部组件相对应) :  
  
  
  
    1.request对象
  
  
  
    客户端的请求信息被封装在request对象中，通过它才能了解到客户的需求，然后做出响应。它是HttpServletRequest类的实例。
  
  
  
    序号 方 法 说 明
  
  
  
    1 object getAttribute(String name) 返回指定属性的属性值
  
  
  
    2 Enumeration getAttributeNames() 返回所有可用属性名的枚举
  
  
  
    3 String getCharacterEncoding() 返回字符编码方式
  
  
  
    4 int getContentLength() 返回请求体的长度 (以字节数) 
  
  
  
    5 String getContentType() 得到请求体的MIME类型
  
  
  
    6 ServletInputStream getInputStream() 得到请求体中一行的二进制流
  
  
  
    7 String getParameter(String name) 返回name指定参数的参数值
  
  
  
    8 Enumeration getParameterNames() 返回可用参数名的枚举
  
  
  
    9 String[] getParameterValues(String name) 返回包含参数name的所有值的数组
  
  
  
    10 String getProtocol() 返回请求用的协议类型及版本号
  
  
  
    11 String getScheme() 返回请求用的计划名,如:http.https及ftp等
  
  
  
    12 String getServerName() 返回接受请求的服务器主机名
  
  
  
    13 int getServerPort() 返回服务器接受此请求所用的端口号
  
  
  
    14 BufferedReader getReader() 返回解码过了的请求体
  
  
  
    15 String getRemoteAddr() 返回发送此请求的客户端IP地址
  
  
  
    16 String getRemoteHost() 返回发送此请求的客户端主机名
  
  
  
    17 void setAttribute(String key,Object obj) 设置属性的属性值
  
  
  
    18 String getRealPath(String path) 返回一虚拟路径的真实路径
  
  
  
    2.response对象
  
  
  
    response对象包含了响应客户请求的有关信息，但在JSP中很少直接用到它。它是HttpServletResponse类的实例。
  
  
  
    序号 方 法 说 明
  
  
  
    1 String getCharacterEncoding() 返回响应用的是何种字符编码
  
  
  
    2 ServletOutputStream getOutputStream() 返回响应的一个二进制输出流
  
  
  
    3 PrintWriter getWriter() 返回可以向客户端输出字符的一个对象
  
  
  
    4 void setContentLength(int len) 设置响应头长度
  
  
  
    5 void setContentType(String type) 设置响应的MIME类型
  
  
  
    6 sendRedirect(java.lang.String location) 重新定向客户端的请求
  
  
  
    3.session对象
  
  
  
    session对象指的是客户端与服务器的一次会话，从客户端连到服务器的一个WebApplication开始，直到客户端与服务器断开连接为止。它是HttpSession类的实例。
  
  
  
    序号 方 法 说 明
  
  
  
    1 long getCreationTime() 返回SESSION创建时间
  
  
  
    2 public String getId() 返回SESSION创建时JSP引擎为它设的惟一ID号
  
  
  
    3 long getLastAccessedTime() 返回此SESSION里客户端最近一次请求时间
  
  
  
    4 int getMaxInactiveInterval() 返回两次请求间隔多长时间此SESSION被取消(ms)
  
  
  
    5 String[] getValueNames() 返回一个包含此SESSION中所有可用属性的数组
  
  
  
    6 void invalidate() 取消SESSION，使SESSION不可用
  
  
  
    7 boolean isNew() 返回服务器创建的一个SESSION,客户端是否已经加入
  
  
  
    8 void removeValue(String name) 删除SESSION中指定的属性
  
  
  
    9 void setMaxInactiveInterval() 设置两次请求间隔多长时间此SESSION被取消(ms)
  
  
  
    4.out对象
  
  
  
    out对象是JspWriter类的实例,是向客户端输出内容常用的对象
  
  
  
    序号 方 法 说 明
  
  
  
    1 void clear() 清除缓冲区的内容
  
  
  
    2 void clearBuffer() 清除缓冲区的当前内容
  
  
  
    3 void flush() 清空流
  
  
  
    4 int getBufferSize() 返回缓冲区以字节数的大小，如不设缓冲区则为0
  
  
  
    5 int getRemaining() 返回缓冲区还剩余多少可用
  
  
  
    6 boolean isAutoFlush() 返回缓冲区满时，是自动清空还是抛出异常
  
  
  
    7 void close() 关闭输出流
  
  
  
    5.page对象
  
  
  
    page对象就是指向当前JSP页面本身，有点象类中的this指针，它是java.lang.Object类的实例
  
  
  
    序号 方 法 说 明
  
  
  
    1 class getClass 返回此Object的类
  
  
  
    2 int hashCode() 返回此Object的hash码
  
  
  
    3 boolean equals(Object obj) 判断此Object是否与指定的Object对象相等
  
  
  
    4 void copy(Object obj) 把此Object拷贝到指定的Object对象中
  
  
  
    5 Object clone() 克隆此Object对象
  
  
  
    6 String toString() 把此Object对象转换成String类的对象
  
  
  
    7 void notify() 唤醒一个等待的线程
  
  
  
    8 void notifyAll() 唤醒所有等待的线程
  
  
  
    9 void wait(int timeout) 使一个线程处于等待直到timeout结束或被唤醒
  
  
  
    10 void wait() 使一个线程处于等待直到被唤醒
  
  
  
    11 void enterMonitor() 对Object加锁
  
  
  
    12 void exitMonitor() 对Object开锁
  
  
  
    6.application对象 
  
  
  
  
  
    application对象实现了用户间数据的共享，可存放全局变量。它开始于服务器的启动，直到服务器的关闭，在此期间，此对象将一直存在；这样在用户的前后连接或不同用户之间的连接中，可以对此对象的同一属性进行操作；在任何地方对此对象属性的操作，都将影响到其他用户对此的访问。服务器的启动和关闭决定了application对象的生命。它是ServletContext类的实例。
  
  
  
    序号 方 法 说 明
  
  
  
    1 Object getAttribute(String name) 返回给定名的属性值
  
  
  
    2 Enumeration getAttributeNames() 返回所有可用属性名的枚举
  
  
  
    3 void setAttribute(String name,Object obj) 设定属性的属性值
  
  
  
    4 void removeAttribute(String name) 删除一属性及其属性值
  
  
  
    5 String getServerInfo() 返回JSP(SERVLET)引擎名及版本号
  
  
  
    6 String getRealPath(String path) 返回一虚拟路径的真实路径
  
  
  
    7 ServletContext getContext(String uripath) 返回指定WebApplication的application对象
  
  
  
    8 int getMajorVersion() 返回服务器支持的Servlet API的最大版本号
  
  
  
    9 int getMinorVersion() 返回服务器支持的Servlet API的最大版本号
  
  
  
    10 String getMimeType(String file) 返回指定文件的MIME类型
  
  
  
    11 URL getResource(String path) 返回指定资源(文件及目录)的URL路径
  
  
  
    12 InputStream getResourceAsStream(String path) 返回指定资源的输入流
  
  
  
    13 RequestDispatcher getRequestDispatcher(String uripath) 返回指定资源的RequestDispatcher对象
  
  
  
    14 Servlet getServlet(String name) 返回指定名的Servlet
  
  
  
    15 Enumeration getServlets() 返回所有Servlet的枚举
  
  
  
    16 Enumeration getServletNames() 返回所有Servlet名的枚举
  
  
  
    17 void log(String msg) 把指定消息写入Servlet的日志文件
  
  
  
    18 void log(Exception exception,String msg) 把指定异常的栈轨迹及错误消息写入Servlet的日志文件
  
  
  
    19 void log(String msg,Throwable throwable) 把栈轨迹及给出的Throwable异常的说明信息 写入Servlet的日志文件
  
  
  
    7.exception对象
  
  
  
    exception对象是一个例外对象，当一个页面在运行过程中发生了例外，就产生这个对象。如果一个JSP页面要应用此对象，就必须把isErrorPage设为true，否则无法编译。他实际上是java.lang.Throwable的对象
  
  
  
    序号 方 法 说 明
  
  
  
    1 String getMessage() 返回描述异常的消息
  
  
  
    2 String toString() 返回关于异常的简短描述消息
  
  
  
    3 void printStackTrace() 显示异常及其栈轨迹
  
  
  
    4 Throwable FillInStackTrace() 重写异常的执行栈轨迹
  
  
  
    8.pageContext对象
  
  
  
    pageContext对象提供了对JSP页面内所有的对象及名字空间的访问，也就是说他可以访问到本页所在的SESSION，也可以取本页面所在的application的某一属性值，他相当于页面中所有功能的集大成者，它的本类名也叫pageContext。
  
  
  
    序号 方 法 说 明
  
  
  
    1 JspWriter getOut() 返回当前客户端响应被使用的JspWriter流(out)
  
  
  
    2 HttpSession getSession() 返回当前页中的HttpSession对象(session)
  
  
  
    3 Object getPage() 返回当前页的Object对象(page)
  
  
  
    4 ServletRequest getRequest() 返回当前页的ServletRequest对象(request)
  
  
  
    5 ServletResponse getResponse() 返回当前页的ServletResponse对象(response)
  
  
  
    6 Exception getException() 返回当前页的Exception对象(exception)
  
  
  
    7 ServletConfig getServletConfig() 返回当前页的ServletConfig对象(config)
  
  
  
    8 ServletContext getServletContext() 返回当前页的ServletContext对象(application)
  
  
  
    9 void setAttribute(String name,Object attribute) 设置属性及属性值
  
  
  
    10 void setAttribute(String name,Object obj,int scope) 在指定范围内设置属性及属性值
  
  
  
    11 public Object getAttribute(String name) 取属性的值
  
  
  
    12 Object getAttribute(String name,int scope) 在指定范围内取属性的值
  
  
  
    13 public Object findAttribute(String name) 寻找一属性,返回起属性值或NULL
  
  
  
    14 void removeAttribute(String name) 删除某属性
  
  
  
    15 void removeAttribute(String name,int scope) 在指定范围删除某属性
  
  
  
    16 int getAttributeScope(String name) 返回某属性的作用范围
  
  
  
    17 Enumeration getAttributeNamesInScope(int scope) 返回指定范围内可用的属性名枚举
  
  
  
    18 void release() 释放pageContext所占用的资源
  
  
  
    19 void forward(String relativeUrlPath) 使当前页面重导到另一页面
  
  
  
    20 void include(String relativeUrlPath) 在当前位置包含另一文件
  
  
  
    9.config对象
  
  
  
    config对象是在一个Servlet初始化时，JSP引擎向它传递信息用的，此信息包括Servlet初始化时所要用到的参数 (通过属性名和属性值构成) 以及服务器的有关信息 (通过传递一个ServletContext对象) 
  
  
  
    序号 方 法 说 明
  
  
  
    1 ServletContext getServletContext() 返回含有服务器相关信息的ServletContext对象
  
  
  
    2 String getInitParameter(String name) 返回初始化参数的值
  
  
  
    3 Enumeration getInitParameterNames() 返回Servlet初始化所需所有参数的枚举
  
