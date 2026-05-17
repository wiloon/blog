---
title: 'The precompilation target directory  cann ot be in the same tree as the source application directory'
author: "-"
date: 2013-07-24T01:10:40+00:00
url: the-precompilation-target-directory-cann-ot-be-in-the-same-tree-as-the-source-application-directory
categories:
  - Inbox
tags:
  - reprint
aliases:
  - /p5697/
---
## 'The precompilation target directory  cann ot be in the same tree as the source application directory'

ASPNETCOMPILER : error ASPRUNTIME: The precompilation target directory (D:appsjenkinsHomejobsxxxworkspacexxxPrecompiledWebxxx) cann
  
ot be in the same tree as the source application directory (D:appsjenkinsHomejobsxxxworkspacexxx). [D:appsjenkinsHomejobsxxx
  
workspacexxxxxx.metaproj]


modify the slution file xxx.sln

modity from

Debug.AspNetCompiler.TargetPath="PrecompiledWebxxx"

Release.AspNetCompiler.TargetPath="PrecompiledWebxxx"

to

Debug.AspNetCompiler.TargetPath="..PrecompiledWebxxx"

Release.AspNetCompiler.TargetPath="..PrecompiledWebxxx"