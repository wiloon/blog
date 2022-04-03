---
title: Remote Debugging | Fitnesse with Eclipse
author: "-"
date: 2012-04-28T02:15:43+00:00
url: /?p=3042
categories:
  - Uncategorized
tags:
  - Fitnesse

---
## Remote Debugging | Fitnesse with Eclipse
In your Eclipse IDE

1. Go to Run->Open Debug Dialog
2. Right click on Remote Java Application option in the left hand menu tree and say new
3. Add the sources to the configuration. These should be all your java projects.These are required so that while remotely debugging you can walk through your code
4. Now your Eclipse configuration is done. Note that we have told eclipse to listen at port 1044 and have specified all the source files that it should use for code walkthrough.
5. Make sure your Fitnesse is up and running.
6. Now add the following line to the fixture that you want to debug:  **!define COMMAND_PATTERN {java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=1044 -cp %p %m}**
7. Start the test in fitnesse
8. Goto Eclipse, open Debug dialog, select the Remote java application that we just created and hit debug button.
9. The debug view would now open at the first breakpoint.
