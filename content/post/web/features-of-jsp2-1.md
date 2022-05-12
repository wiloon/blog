---
title: Features of jsp2.1
author: "-"
date: 2012-09-22T07:33:03+00:00
url: /?p=4179
categories:
  - Java
tags:$
  - reprint
---
## Features of jsp2.1
<http://www.roseindia.net/jsp/FeaturesOfJsp2.1.shtml>

The main purpose of Java Platform, Enterprise Edition (Java EE) 5 is to ease development. Now the Jsp2.1 includes theJava Standard Tag Library(JSTL) and JavaServerFaces technology.


This version has new expression language (EL ) syntax that allows deferred evaluation of expressions. It now enables using the expression to both get and set data and to invoke methods, and facilitates customizing the resolution of a variable or property referenced by an expression.

It supports resource injection through annotations to simplify configuring access to resources and environment data.

It has complete alignment of JSF technology tags and JSP software code. Earlier the version 1.0 of jsf technology depended on jsp 1.2 technology. The reason is that the Jsp 1.2 was already available at the time, and the intension was to make the Jsf 1.0 interface more accessible to a broader audience. As jsp1.2 does not have an integrated expression language and because the Jsp 2.0 EL does not meet all of the needs of Jsf, therefore jsp2.1 was developed to enhance the expression language to meet the needs of Jsf technology.

Qualified functions now take precedence over the ternary operator when the "." operator in use or we can say that ability to redefine the behavior of the "."operator through a Property ResolverAPI.

EL now supports "literal expressions". The expression which were previously considered to be non-EL value text must now be considered an EL expression.

EL now supports Java 5.0 enumerations.

Ability to plug in Property Resolvers on a per-application and per-page basis.

Ability to express references to bean methods using the expression language and invoking those methods via a Method Binding API.

This version requires these jars:


1) ant-1.6.5.jar


2) core-3.1.1.jar


3 jsp-2.1.jar


4) jsp-api-2.1.jar