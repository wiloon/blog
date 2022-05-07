---
title: Compare Plain File
author: lcf
date: 2012-10-29T03:21:59+00:00
url: /?p=4563
categories:
  - Inbox
tags:
  - reprint
---
## Compare Plain File

'///////////////////////////////////////////////////////////////////////////////////////////////////////////
  
'
  
' Compare two plain file in row-to-row
  
' Return Code: 1 = same; 0=difference
  
'
  
'//////////////////////////////////////////////////////////////////////////////////////////////////////////
  
public Function ComparePlainFile(cFile1, cFile2)
  
On Error Resume Next
  
ComparePlainFile = 1
  
Const ForReading = 1
  
Dim fso, txtFile1, strLine1, txtFile2, strLine2

Set fso = CreateObject("Scripting.FileSystemObject")
  
Set txtFile1 = fso.OpenTextFile(cFile1, ForReading)
  
Set txtFile2 = fso.OpenTextFile(cFile2, ForReading)
  
Do Until txtFile1.AtEndOfStream or txtFile2.AtEndOfStream
  
strLine1 = trim(txtFile1.ReadLine)
  
strLine2 = trim(txtFile2.ReadLine)
  
If strLine1<>strLine2 Then
  
ComparePlainFile = 0
  
Exit do
  
End If
  
Loop

txtFile1.close()
  
Set txtFile1 = Nothing
  
txtFile2.close()
  
Set txtFile2 = Nothing
  
Set fso = nothing

End Function