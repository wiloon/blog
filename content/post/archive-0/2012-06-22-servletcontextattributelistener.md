---
title: ServletContextAttributeListener
author: wiloon
type: post
date: 2012-06-22T03:26:20+00:00
url: /?p=3588
categories:
  - Uncategorized

---
<pre><span style="color: #ff0000;"> ServletContext context = getServletContext();</span><br />
<span style="color: #ff0000;"> context.setAttribute("attrName", "attrValue");</span><br />
[java]</p>


<p>
  import javax.servlet.ServletContext;<br />
  import javax.servlet.ServletException;<br />
  import javax.servlet.http.HttpServlet;<br />
  import javax.servlet.http.HttpServletRequest;<br />
  import javax.servlet.http.HttpServletResponse;<br />
  import java.io.IOException;<br />
  import java.io.PrintWriter;<br />
  import java.util.Enumeration;
</p>


<p>
  public class HelloWorld extends HttpServlet {
</p>


<p>
  private static final long serialVersionUID = -9037964452251358377L;
</p>


<p>
  public HelloWorld() {<br />
   System.out.println("servlet.helloWorld.constructor");<br />
   }
</p>


<p>
  public void init() {<br />
   System.out.println("servlet.helloWorld.init.");<br />
   }
</p>


<p>
  public void destroy() {<br />
   System.out.println("servlet.helloWorld.destroy.");<br />
   }
</p>


<p>
  public void doGet(HttpServletRequest request, HttpServletResponse response)<br />
   throws ServletException, IOException {<br />
   System.out.println("servlet.helloWorld.doGet.start");
</p>


<p>
  // get, query string<br />
   String queryString = request.getQueryString();
</p>


<p>
  // header name<br />
   printHeaderName(request);
</p>


<p>
  // get parameter<br />
   System.out.println("parameter.foo= " + request.getParameter("foo"));
</p>


<p>
  // query string<br />
   System.out.println("query string: " + queryString);
</p>


<p>
  // character encoding<br />
   System.out.println("encoding: " + request.getCharacterEncoding());
</p>


<p>
  //init param<br />
   System.out.println("init param: " + getInitParameter("ipn"));
</p>


<p>
  //set context attribute<br />
   ServletContext context = getServletContext();<br />
   context.setAttribute("attrName", "attrValue");
</p>


<p>
  response.setContentType("text/html");<br />
   PrintWriter out = response.getWriter();<br />
   out.println("<html><head><title>");<br />
   out.println("This is my first Servlet");<br />
   out.println("</title></head><body>");<br />
   out.println("<h1>Hello,World!, Servlet!</h1>");<br />
   out.println("</body></html>");
</p>


<p>
  System.out.println("servlet.helloWorld.doGet.end");<br />
   }
</p>


<p>
  private void printHeaderName(HttpServletRequest request) {<br />
   Enumeration enumstr = request.getHeaderNames();
</p>


<p>
  while (enumstr.hasMoreElements()) {<br />
   String name = (String) enumstr.nextElement();<br />
   System.out.println("header: " + name + " = "<br />
   + request.getHeader(name));
</p>


<p>
  }
</p>


<p>
  }
</p>


<p>
  public void doPost(HttpServletRequest request, HttpServletResponse response)<br />
   throws ServletException, IOException {<br />
   // post, request form<br />
   // String form = request.get;<br />
   }<br />
  }
</p>


<p>
  [/java]
</p>