---
title: tomcat 8005
author: "-"
date: 2012-05-13T11:16:08+00:00
url: /?p=3122
categories:
  - Web
tags:
  - Tomcat

---
## tomcat 8005
[http://www.wellho.net/mouth/837_Tomcat-Shutdown-port.html](http://www.wellho.net/mouth/837_Tomcat-Shutdown-port.html)

  On a new installation of Tomcat (default config files), you'll notice that your server.xml file is set up with a shutdown port of 8005, and shutdown="SHUTDOWN". What does this mean? 
  
    It means that anyone who contacts the server locally on port 8005 and send it the words SHUTDOWN can cause Tomcat to close out all its web applications and shut down cleanly. Yikes - is this a security hole of what? It could be. Fortunatly , you'll notice that I said it's a LOCAL connection to the port that causes a shutdown, so it no-one can ssh or telnet in, nor log in from the keyboard unless they're an admin, it might not be a problem ....
  
  
    If your Tomcat server allows anyone except the administrator to log in with a shell, then I strongly suggest you change shutdown="SHUTDOWN" to shutdown="waSS-I41tis" so that at least it won't be a string that any hacker can guess.<del> You might like to change the port number too. Alas, it would be unwise to disable the facility completely, since catalina.sh and shutdown.sh use the port (details read from the config file) as part of their processing. At least server.xml is neither group nor world readable.</del> 
    
    
    
    
    
    