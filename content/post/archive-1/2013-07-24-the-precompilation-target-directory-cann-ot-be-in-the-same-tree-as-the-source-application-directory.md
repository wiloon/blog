---
title: 'The precompilation target directory  cann ot be in the same tree as the source application directory'
author: wiloon
type: post
date: 2013-07-24T01:10:40+00:00
url: /?p=5697
categories:
  - Uncategorized

---
ASPNETCOMPILER : error ASPRUNTIME: The precompilation target directory (D:appsjenkinsHomejobsxxxworkspacexxxPrecompiledWebxxx) cann
  
ot be in the same tree as the source application directory (D:appsjenkinsHomejobsxxxworkspacexxx). [D:appsjenkinsHomejobsxxx
  
workspacexxxxxx.metaproj]



modify the slution file xxx.sln

modity from

Debug.AspNetCompiler.TargetPath=&#8221;PrecompiledWebxxx&#8221;

Release.AspNetCompiler.TargetPath=&#8221;PrecompiledWebxxx&#8221;

to

Debug.AspNetCompiler.TargetPath=&#8221;..PrecompiledWebxxx&#8221;

Release.AspNetCompiler.TargetPath=&#8221;..PrecompiledWebxxx&#8221;