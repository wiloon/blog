---
title: java exit code
author: wiloon
type: post
date: 2015-12-30T07:25:26+00:00
url: /?p=8612
categories:
  - Uncategorized

---
<div id="post_message_193890">
  http://blog.sina.com.cn/s/blog_5396eb53010004sg.html
</div>

<div>
  The number is only the status code for the termination of the JVM. It does not effect the actual command. By convention 0 means a normal exit, anything else signifies an abnormal termination.
</div>

<div>
  <div id="post_message_193968">
    You can actually return any int not just a 1 or 0. A common <a id="KonaLink0" class="kLink" href="http://www.linuxquestions.org/questions/showthread.php?t=39993#" target="_top" name="KonaLink0"><span style="color: blue;"><span class="kLink">Unix</span></span></a> programming convention is to upon completion of your program return an exit status which can be used to determine if the program executed successfully. Generally speaking "0&#8221; means success and otherwise indicates that your program returned unexpected results (not necessarily failure). This is so you can glue a bunch of general purpose programs together (e.g.: using a <a id="KonaLink1" class="kLink" href="http://www.linuxquestions.org/questions/showthread.php?t=39993#" target="_top" name="KonaLink1"><span style="color: blue;"><span class="kLink">shell</span> <span class="kLink">script</span></span></a>) and allows you to exit gracefully if something does not happen the way it was intended to happen. A good example of this is to look at the grep man page. Exit 0 means the text you were <a id="KonaLink2" class="kLink" href="http://www.linuxquestions.org/questions/showthread.php?t=39993#" target="_top" name="KonaLink2"><span style="color: blue;"><span class="kLink">searching</span></span></a> for was found, Exit 1 means that the text you were searching for was not found and Exit 2 means it barfed.</p> 
    
    <p>
      To get a handle no the exit status, the env variable “$?” is the return status of the last command. So try this:
    </p>
    
    <p>
      bash$ cat “SOME_FILE_THAT_DOES_NOT_EXIST”
 bash$ echo $?
 and your result should be 1.
    </p>
    
    <p>
      bash$ cat “SOME_FILE_THAT_DOES_EXIST”
 bash$ echo $?
 and your result should be 0.
    </p>
    
    <p>
      hope this helps,
 cludwin
    </p>
  </div>
</div>