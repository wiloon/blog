---
title: System.exit(n)
author: "-"
date: 2017-01-06T06:55:57+00:00
url: /?p=9642
categories:
  - Inbox
tags:
  - reprint
---
## System.exit(n)
http://www.cnblogs.com/xwdreamer/archive/2011/01/07/2297045.html

1.参考文献
  
http://hi.baidu.com/accpzhangbo/blog/item/52aeffc683ee6ec238db4965.html

2.解析
  
查看java.lang.System的源代码,我们可以找到System.exit(status)这个方法的说明,代码如下: 
  
/**
  
* Terminates the currently running Java Virtual Machine. The
  
* argument serves as a status code; by convention, a nonzero status
  
* code indicates abnormal termination.
  
* 
  
* This method calls the exit method in class
  
* Runtime. This method never returns normally.
  
* 
  
* The call System.exit(n) is effectively equivalent to
  
* the call:
  
* 
  
* Runtime.getRuntime().exit(n)
  
* 
  
*
  
* @param status exit status.
  
* @throws SecurityException
  
* if a security manager exists and its checkExit
  
* method doesn't allow exit with the specified status.
  
* @see java.lang.Runtime#exit(int)
  
*/
  
public static void exit(int status) {
  
Runtime.getRuntime().exit(status);
  
}

注释中说的很清楚,这个方法是用来结束当前正在运行中的java虚拟机。如何status是非零参数,那么表示是非正常退出。

System.exit(0)是将你的整个虚拟机里的内容都停掉了 ,而dispose()只是关闭这个窗口,但是并没有停止整个application exit() 。无论如何,内存都释放了！也就是说连JVM都关闭了,内存里根本不可能还有什么东西
  
System.exit(0)是正常退出程序,而System.exit(1)或者说非0表示非正常退出程序
  
System.exit(status)不管status为何值都会退出程序。和return 相比有以下不同点: return是回到上一层,而System.exit(status)是回到最上层
  
3.示例
  
在一个if-else判断中,如果我们程序是按照我们预想的执行,到最后我们需要停止程序,那么我们使用System.exit(0),而System.exit(1)一般放在catch块中,当捕获到异常,需要停止程序,我们使用System.exit(1)。这个status=1是用来表示这个程序是非正常退出。