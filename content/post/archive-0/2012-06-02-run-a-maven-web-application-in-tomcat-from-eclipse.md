---
title: run a maven web application in Tomcat from Eclipse
author: wiloon
type: post
date: 2012-06-02T01:30:36+00:00
url: /?p=3310
categories:
  - Java
  - Web
tags:
  - Tomcat

---
An Eclipse User Library can be used to represent a set of jar files. This user library can be added to a project&#8217;s classpath. Thus, a user library can be a convenient way to add a set of jar files (rather than individual jar files) to a project&#8217;s build path. Here, I&#8217;ll create a user library for a set of Tomcat jar files.

To create a user library, you can go to Window → Preferences and go to Java → Build Path → User Libraries. I&#8217;ll click the New button to create a new user library.

I named my new user library "TOMCAT\_6.0.14\_LIBRARY" and clicked OK.

I selected TOMCAT\_6.0.14\_LIBRARY and clicked the "Add JARs" button.

I browsed to my Tomcat bin directory and selected 3 jar files, including the bootstrap.jar file. I added these to my user library.

Next, I clicked Add JARs again and this time browsed to my Tomcat lib directory and selected several jar files, shown below.

When done, my TOMCAT\_6.0.14\_LIBRARY consisted of several jar files, shown below. I clicked OK to save this library.

After doing this, if I have a web application project that will run in Tomcat in Eclipse, I can add the TOMCAT\_6.0.14\_LIBRARY to the classpath to have all the necessary Tomcat jar files automatically added to the project&#8217;s classpath.

I&#8217;d like to update my project&#8217;s pom.xml file so that if I execute the eclipse:eclipse goal on my project, it will update the project&#8217;s classpathW to include the Tomcat user library.

Here is the "mywebapp" project&#8217;s original pom.xml file.

### original pom.xml

&lt;project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd"&gt;
  &lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;
  &lt;groupId&gt;com.maventest&lt;/groupId&gt;
  &lt;artifactId&gt;mywebapp&lt;/artifactId&gt;
  &lt;packaging&gt;war&lt;/packaging&gt;
  &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
  &lt;name&gt;mywebapp Maven Webapp&lt;/name&gt;
  &lt;url&gt;http://maven.apache.org&lt;/url&gt;
  &lt;dependencies&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;junit&lt;/groupId&gt;
      &lt;artifactId&gt;junit&lt;/artifactId&gt;
      &lt;version&gt;3.8.1&lt;/version&gt;
      &lt;scope&gt;test&lt;/scope&gt;
    &lt;/dependency&gt;
  &lt;/dependencies&gt;
  &lt;build&gt;
    &lt;finalName&gt;mywebapp&lt;/finalName&gt;
  &lt;/build&gt;
&lt;/project&gt;

I&#8217;ll update the "mywebapp" project&#8217;s pom.xml file to include a plugin reference to the maven-eclipse-plugin. I add a configuration section that specifies that the "org.eclipse.jdt.launching.JRE\_CONTAINER" and "org.eclipse.jdt.USER\_LIBRARY/TOMCAT\_6.0.14\_LIBRARY" classpath containers will be added to the classpath when eclipse:eclipse is executed. The JRE\_CONTAINER is specified since it is there already. Notice the format in which the Tomcat user library is specified (it begins with "org.eclipse.jdt.USER\_LIBRARY/").

### updated pom.xml

&lt;project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd"&gt;
	&lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;
	&lt;groupId&gt;com.maventest&lt;/groupId&gt;
	&lt;artifactId&gt;mywebapp&lt;/artifactId&gt;
	&lt;packaging&gt;war&lt;/packaging&gt;
	&lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
	&lt;name&gt;mywebapp Maven Webapp&lt;/name&gt;
	&lt;url&gt;http://maven.apache.org&lt;/url&gt;
	&lt;dependencies&gt;
		&lt;dependency&gt;
			&lt;groupId&gt;junit&lt;/groupId&gt;
			&lt;artifactId&gt;junit&lt;/artifactId&gt;
			&lt;version&gt;3.8.1&lt;/version&gt;
			&lt;scope&gt;test&lt;/scope&gt;
		&lt;/dependency&gt;
	&lt;/dependencies&gt;
	&lt;build&gt;
		&lt;finalName&gt;mywebapp&lt;/finalName&gt;
		&lt;plugins&gt;
			&lt;plugin&gt;
				&lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
				&lt;artifactId&gt;maven-eclipse-plugin&lt;/artifactId&gt;
				&lt;inherited&gt;true&lt;/inherited&gt;
				&lt;configuration&gt;
					&lt;classpathContainers&gt;
						&lt;classpathContainer&gt;org.eclipse.jdt.launching.JRE_CONTAINER&lt;/classpathContainer&gt;
						&lt;classpathContainer&gt;org.eclipse.jdt.USER_LIBRARY/TOMCAT_6.0.14_LIBRARY&lt;/classpathContainer&gt;
					&lt;/classpathContainers&gt;
				&lt;/configuration&gt;
			&lt;/plugin&gt;
		&lt;/plugins&gt;
	&lt;/build&gt;
&lt;/project&gt;

Now, I&#8217;ll run "mvn eclipse:eclipse" on the "mywebapp" project via an Eclipse external tool configuration.

Before running eclipse:eclipse, the "mywebapp" .classpath file looked like this:

### .classpath file before pom.xml update

&lt;classpath&gt;
  &lt;classpathentry kind="src" path="src/main/resources" excluding="**/*.java"/&gt;
  &lt;classpathentry kind="output" path="target/classes"/&gt;
  &lt;classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER"/&gt;
  &lt;classpathentry kind="var" path="M2_REPO/junit/junit/3.8.1/junit-3.8.1.jar"/&gt;
&lt;/classpath&gt;

After running eclipse:eclipse, the "mywebapp" .classpath file was updated to look like this:

### .classpath file after pom.xml update

&lt;classpath&gt;
  &lt;classpathentry kind="src" path="src/main/resources" excluding="**/*.java"/&gt;
  &lt;classpathentry kind="output" path="target/classes"/&gt;
  &lt;classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER"/&gt;
  &lt;classpathentry kind="con" path="org.eclipse.jdt.USER_LIBRARY/TOMCAT_6.0.14_LIBRARY"/&gt;
  &lt;classpathentry kind="var" path="M2_REPO/junit/junit/3.8.1/junit-3.8.1.jar"/&gt;
&lt;/classpath&gt;

The "mywebapp" project now has the TOMCAT\_6.0.14\_LIBRARY user library included in its classpath!

So, let&#8217;s get started. First of all, I need to add a Context entry to my Tomcat&#8217;s server.xml file for the "mywebapp" project. In Eclipse, I have a "_stuff" project that contains a link to my Tomcat&#8217;s server.xml file for convenience. So, I&#8217;ll double-click the server.xml link to open up the server.xml file in Eclipse&#8217;s XMLWeditor.

I&#8217;ll add the following Context element to my Tomcat server.xml file. The docBase attribute specifies my web context directory (ie, web, public_html, webapp, etc..) for my project. The path attribute specifies the path that is used to hit the project via a web browser (ie, http://localhost:8080/mywebapp).

&lt;Context docBase="C:devworkspacemywebappsrcmainwebapp" path="/mywebapp" reloadable="true"/&gt;

The server.xml file is shown below. Notice that the <Context> element is within the <Host> element.

Now, I&#8217;ll create an EclipseSW Debug Configuration to start up my project in TomcatSW. I named the Debug Configuration "mywebapp tomcat". I specified the project to be "mywebapp". The Tomcat main class from the bootstrap.jar file is "org.apache.catalina.startup.Bootstrap".

On the Arguments tab, I specified the working directory to be my Tomcat home directory, which for me is C:devapache-tomcat-6.0.14.


  
    I clicked the Debug button to start up my project in Tomcat via Eclipse.
  
  
  
    I went to a web browser and attempted to hit my "mywebapp" web application via http://localhost:8080/mywebapp. It worked!
  
  
  
    <a href="http://www.avajava.com/tutorials/lessons/how-do-i-run-a-maven-web-application-in-tomcat-from-eclipse.html?page=1">http://www.avajava.com/tutorials/lessons/how-do-i-run-a-maven-web-application-in-tomcat-from-eclipse.html?page=1</a>
  


http://www.avajava.com/tutorials/lessons/how-do-i-create-an-eclipse-user-library-for-the-tomcat-jar-files.html

http://www.avajava.com/tutorials/lessons/how-do-i-update-my-classpath-with-an-eclipse-user-library-via-the-maven-eclipse-plugin.html

<http://www.avajava.com/tutorials/lessons/how-do-i-debug-my-web-project-in-tomcat-from-eclipse.html?page=1>