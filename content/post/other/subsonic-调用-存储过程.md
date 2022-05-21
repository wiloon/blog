---
title: subsonic 调用 存储过程
author: "-"
date: 2013-06-27T08:18:32+00:00
url: /?p=5579
categories:
  - Inbox
tags:
  - reprint
---
## subsonic 调用 存储过程

[csharp]
  
public static int GetRUID(string tblName)
  
{
  
StoredProcedure spd = new StoredProcedure("GenerateRUID");
  
spd.Command.AddParameter("@tblName", tblName);
  
spd.Command.AddOutputParameter("@currentnumber");
  
spd.Execute();
  
int currentnumber = int.Parse(spd.OutputValues[0].ToString());
  
return currentnumber;
  
}
  
[/csharp]
