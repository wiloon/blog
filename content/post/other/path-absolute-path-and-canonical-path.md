---
title: path, absolute path, and canonical path
author: "-"
date: 2011-09-13T11:39:24+00:00
url: /?p=772
categories:
  - Java

tags:
  - reprint
---
## path, absolute path, and canonical path
http://www.avajava.com/tutorials/lessons/whats-the-difference-between-a-files-path-absolute-path-and-canonical-path.html
  
-
  
What's the difference between a file's path, absolute path, and canonical path?
  
Author: Deron Eriksson
  
Description: This Java tutorial describes a file's path, absolute path, and canonical path.
  
Tutorial created using: Windows XP || JDK 1.5.0_09 || Eclipse Web Tools Platform 2.0 (Eclipse 3.3.0)

This tutorial will examine the differences between a file's path, absolute path, and canonical path. The FilePaths class will display data about several files and directories in the project. In JavaSW, a File object can represent a file or a directory. If a File object represents a directory, a call to its isDirectory() method returns true. Our project consists of the FilePaths class plus several files and directories.

The FilePaths class is shown below. It displays information including path information for five files/directories in the project.

FilePaths.java

package test;

import java.io.File;
  
import java.io.IOException;

public class FilePaths {

public static void main(String[] args) throws IOException {

String[] fileArray = {
                  
"C:\projects\workspace\testing\f1\f2\f3\file5.txt",
                  
"folder/file3.txt",
                  
"../testing/file1.txt",
                  
"../testing",
                  
"f1/f2"
          
};

for (String f : fileArray) {
              
displayInfo(f);
          
}

}

public static void displayInfo(String f) throws IOException {
          
File file = new File(f);
          
System.out.println("========================================");
          
System.out.println(" name:" + file.getName());
          
System.out.println(" is directory:" + file.isDirectory());
          
System.out.println(" exists:" + file.exists());
          
System.out.println(" path:" + file.getPath());
          
System.out.println(" absolute file:" + file.getAbsoluteFile());
          
System.out.println(" absolute path:" + file.getAbsolutePath());
          
System.out.println("canonical file:" + file.getCanonicalFile());
          
System.out.println("canonical path:" + file.getCanonicalPath());
      
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

Next, you should notice that getPath() returns the file path that we used when we instantiated the File object with the String file path, but with the current system's path separation character. Since I'm on Windows XP, this is a backslash. If this path is relative, getPath() returns the relative path, whereas if we specified a full path when instantiating the File object, the full path is returned by getPath(). The getPath() method also returns "." and ".." if we used them in specifying the relative path.

Next, notice that getAbsolutePath() returns an absolute path, but that this path can contain things like "." and "..". The getCanonicalPath() method, on the other hand, returns an absolute path, but it removes unnecessary parts of the path, such as "." and ".." and any other unnecessary directories involved in the "." or ".." path. This is shown clearly in the file1.txt example above.

On Windows systems, the getCanonicalPath() method will also uppercase the drive letter. As an example, if we passed the following file string with a lowercase drive letter to displayInfo()

"c:\projects\workspace\testing\f1\f2\f3\file5.txt"
  
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