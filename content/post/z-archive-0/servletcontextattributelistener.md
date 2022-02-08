---
title: ServletContextAttributeListener
author: "-"
date: 2012-06-22T03:26:20+00:00
url: /?p=3588
categories:
  - Uncategorized

tags:
  - reprint
---
## ServletContextAttributeListener
 ServletContext context = getServletContext();

 context.setAttribute("attrName", "attrValue");

```java


  import javax.servlet.ServletContext;

  import javax.servlet.ServletException;

  import javax.servlet.http.HttpServlet;

  import javax.servlet.http.HttpServletRequest;

  import javax.servlet.http.HttpServletResponse;

  import java.io.IOException;

  import java.io.PrintWriter;

  import java.util.Enumeration;


  public class HelloWorld extends HttpServlet {


  private static final long serialVersionUID = -9037964452251358377L;


  public HelloWorld() {

   System.out.println("servlet.helloWorld.constructor");

   }


  public void init() {

   System.out.println("servlet.helloWorld.init.");

   }


  public void destroy() {

   System.out.println("servlet.helloWorld.destroy.");

   }


  public void doGet(HttpServletRequest request, HttpServletResponse response)

   throws ServletException, IOException {

   System.out.println("servlet.helloWorld.doGet.start");


  // get, query string

   String queryString = request.getQueryString();


  // header name

   printHeaderName(request);


  // get parameter

   System.out.println("parameter.foo= " + request.getParameter("foo"));


  // query string

   System.out.println("query string: " + queryString);


  // character encoding

   System.out.println("encoding: " + request.getCharacterEncoding());


  //init param

   System.out.println("init param: " + getInitParameter("ipn"));


  //set context attribute

   ServletContext context = getServletContext();

   context.setAttribute("attrName", "attrValue");


  response.setContentType("text/html");

   PrintWriter out = response.getWriter();

   out.println("<html><head><title>");

   out.println("This is my first Servlet");

   out.println("</title></head><body>");

   out.println("Hello,World!, Servlet!");

   out.println("</body></html>");


  System.out.println("servlet.helloWorld.doGet.end");

   }


  private void printHeaderName(HttpServletRequest request) {

   Enumeration enumstr = request.getHeaderNames();


  while (enumstr.hasMoreElements()) {

   String name = (String) enumstr.nextElement();

   System.out.println("header: " + name + " = "

   + request.getHeader(name));


  }


  }


  public void doPost(HttpServletRequest request, HttpServletResponse response)

   throws ServletException, IOException {

   // post, request form

   // String form = request.get;

   }

  }


  ```
