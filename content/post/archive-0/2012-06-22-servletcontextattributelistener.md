---
title: ServletContextAttributeListener
author: wiloon
type: post
date: 2012-06-22T03:26:20+00:00
url: /?p=3588
categories:
  - Uncategorized

---
<pre><span style="color: #ff0000;"> ServletContext context = getServletContext();</span>

<span style="color: #ff0000;"> context.setAttribute("attrName", "attrValue");</span>

[java]</p>


<p>
  import javax.servlet.ServletContext;

  import javax.servlet.ServletException;

  import javax.servlet.http.HttpServlet;

  import javax.servlet.http.HttpServletRequest;

  import javax.servlet.http.HttpServletResponse;

  import java.io.IOException;

  import java.io.PrintWriter;

  import java.util.Enumeration;
</p>


<p>
  public class HelloWorld extends HttpServlet {
</p>


<p>
  private static final long serialVersionUID = -9037964452251358377L;
</p>


<p>
  public HelloWorld() {

   System.out.println("servlet.helloWorld.constructor");

   }
</p>


<p>
  public void init() {

   System.out.println("servlet.helloWorld.init.");

   }
</p>


<p>
  public void destroy() {

   System.out.println("servlet.helloWorld.destroy.");

   }
</p>


<p>
  public void doGet(HttpServletRequest request, HttpServletResponse response)

   throws ServletException, IOException {

   System.out.println("servlet.helloWorld.doGet.start");
</p>


<p>
  // get, query string

   String queryString = request.getQueryString();
</p>


<p>
  // header name

   printHeaderName(request);
</p>


<p>
  // get parameter

   System.out.println("parameter.foo= " + request.getParameter("foo"));
</p>


<p>
  // query string

   System.out.println("query string: " + queryString);
</p>


<p>
  // character encoding

   System.out.println("encoding: " + request.getCharacterEncoding());
</p>


<p>
  //init param

   System.out.println("init param: " + getInitParameter("ipn"));
</p>


<p>
  //set context attribute

   ServletContext context = getServletContext();

   context.setAttribute("attrName", "attrValue");
</p>


<p>
  response.setContentType("text/html");

   PrintWriter out = response.getWriter();

   out.println("<html><head><title>");

   out.println("This is my first Servlet");

   out.println("</title></head><body>");

   out.println("<h1>Hello,World!, Servlet!</h1>");

   out.println("</body></html>");
</p>


<p>
  System.out.println("servlet.helloWorld.doGet.end");

   }
</p>


<p>
  private void printHeaderName(HttpServletRequest request) {

   Enumeration enumstr = request.getHeaderNames();
</p>


<p>
  while (enumstr.hasMoreElements()) {

   String name = (String) enumstr.nextElement();

   System.out.println("header: " + name + " = "

   + request.getHeader(name));
</p>


<p>
  }
</p>


<p>
  }
</p>


<p>
  public void doPost(HttpServletRequest request, HttpServletResponse response)

   throws ServletException, IOException {

   // post, request form

   // String form = request.get;

   }

  }
</p>


<p>
  [/java]
</p>