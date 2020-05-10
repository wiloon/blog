---
title: path, absolute path, and canonical path
author: wiloon
type: post
date: 2011-09-13T11:39:24+00:00
url: /?p=772
bot_views:
  - 8
views:
  - 2
categories:
  - Java

---
http://www.avajava.com/tutorials/lessons/whats-the-difference-between-a-files-path-absolute-path-and-canonical-path.html
  
&#8212;
  
What&#8217;s the difference between a file&#8217;s path, absolute path, and canonical path?
  
Author: Deron Eriksson
  
Description: This Java tutorial describes a file&#8217;s path, absolute path, and canonical path.
  
Tutorial created using: Windows XP || JDK 1.5.0_09 || Eclipse Web Tools Platform 2.0 (Eclipse 3.3.0)

This tutorial will examine the differences between a file&#8217;s path, absolute path, and canonical path. The FilePaths class will display data about several files and directories in the project. In JavaSW, a File object can represent a file or a directory. If a File object represents a directory, a call to its isDirectory() method returns true. Our project consists of the FilePaths class plus several files and directories.

The FilePaths class is shown below. It displays information including path information for five files/directories in the project.

FilePaths.java

package test;

import java.io.File;
  
import java.io.IOException;

public class FilePaths {

public static void main(String[] args) throws IOException {

String[] fileArray = {
				  
&#8220;C:\projects\workspace\testing\f1\f2\f3\file5.txt&#8221;,
				  
&#8220;folder/file3.txt&#8221;,
				  
&#8220;../testing/file1.txt&#8221;,
				  
&#8220;../testing&#8221;,
				  
&#8220;f1/f2&#8221;
		  
};

for (String f : fileArray) {
			  
displayInfo(f);
		  
}

}

public static void displayInfo(String f) throws IOException {
		  
File file = new File(f);
		  
System.out.println(&#8220;========================================&#8221;);
		  
System.out.println(&#8221; name:&#8221; + file.getName());
		  
System.out.println(&#8221; is directory:&#8221; + file.isDirectory());
		  
System.out.println(&#8221; exists:&#8221; + file.exists());
		  
System.out.println(&#8221; path:&#8221; + file.getPath());
		  
System.out.println(&#8221; absolute file:&#8221; + file.getAbsoluteFile());
		  
System.out.println(&#8221; absolute path:&#8221; + file.getAbsolutePath());
		  
System.out.println(&#8220;canonical file:&#8221; + file.getCanonicalFile());
		  
System.out.println(&#8220;canonical path:&#8221; + file.getCanonicalPath());
	  
}

}
  
Executing FilePaths results in the following output:

========================================
            
name:file5.txt
    
is directory:false
          
exists:true
            
path:C:projectsworkspacetestingf1f2f3file5.txt
   
absolute file:C:projectsworkspacetestingf1f2f3file5.txt
   
absolute path:C:projectsworkspacetestingf1f2f3file5.txt
  
canonical file:C:projectsworkspacetestingf1f2f3file5.txt
  
canonical path:C:projectsworkspacetestingf1f2f3file5.txt
  
========================================
            
name:file3.txt
    
is directory:false
          
exists:true
            
path:folderfile3.txt
   
absolute file:C:projectsworkspacetestingfolderfile3.txt
   
absolute path:C:projectsworkspacetestingfolderfile3.txt
  
canonical file:C:projectsworkspacetestingfolderfile3.txt
  
canonical path:C:projectsworkspacetestingfolderfile3.txt
  
========================================
            
name:file1.txt
    
is directory:false
          
exists:true
            
path:..testingfile1.txt
   
absolute file:C:projectsworkspacetesting..testingfile1.txt
   
absolute path:C:projectsworkspacetesting..testingfile1.txt
  
canonical file:C:projectsworkspacetestingfile1.txt
  
canonical path:C:projectsworkspacetestingfile1.txt
  
========================================
            
name:testing
    
is directory:true
          
exists:true
            
path:..testing
   
absolute file:C:projectsworkspacetesting..testing
   
absolute path:C:projectsworkspacetesting..testing
  
canonical file:C:projectsworkspacetesting
  
canonical path:C:projectsworkspacetesting
  
========================================
            
name:f2
    
is directory:true
          
exists:true
            
path:f1f2
   
absolute file:C:projectsworkspacetestingf1f2
   
absolute path:C:projectsworkspacetestingf1f2
  
canonical file:C:projectsworkspacetestingf1f2
  
canonical path:C:projectsworkspacetestingf1f2
  
Looking at the output tells us about path, absolute file, absolute path, canonical file, and canonical path. First off, you probably noticed that getAbsoluteFile() returns the same result as getAbsolutePath(), and getCanonicalFile() returns the same result as getCanonicalPath().

Next, you should notice that getPath() returns the file path that we used when we instantiated the File object with the String file path, but with the current system&#8217;s path separation character. Since I&#8217;m on Windows XP, this is a backslash. If this path is relative, getPath() returns the relative path, whereas if we specified a full path when instantiating the File object, the full path is returned by getPath(). The getPath() method also returns &#8220;.&#8221; and &#8220;..&#8221; if we used them in specifying the relative path.

Next, notice that getAbsolutePath() returns an absolute path, but that this path can contain things like &#8220;.&#8221; and &#8220;..&#8221;. The getCanonicalPath() method, on the other hand, returns an absolute path, but it removes unnecessary parts of the path, such as &#8220;.&#8221; and &#8220;..&#8221; and any other unnecessary directories involved in the &#8220;.&#8221; or &#8220;..&#8221; path. This is shown clearly in the file1.txt example above.

On Windows systems, the getCanonicalPath() method will also uppercase the drive letter. As an example, if we passed the following file string with a lowercase drive letter to displayInfo()

&#8220;c:\projects\workspace\testing\f1\f2\f3\file5.txt&#8221;
  
we would see the following result:

========================================
            
name:file5.txt
    
is directory:false
          
exists:true
            
path:c:projectsworkspacetestingf1f2f3file5.txt
   
absolute file:c:projectsworkspacetestingf1f2f3file5.txt
   
absolute path:c:projectsworkspacetestingf1f2f3file5.txt
  
canonical file:C:projectsworkspacetestingf1f2f3file5.txt
  
canonical path:C:projectsworkspacetestingf1f2f3file5.txt
  
Notice that getPath() and getAbsolutePath() return the lowercase drive letter that we entered, but getCanonicalPath() returns the uppercase drive letter.