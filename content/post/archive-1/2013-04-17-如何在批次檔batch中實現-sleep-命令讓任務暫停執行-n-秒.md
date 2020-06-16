---
title: bat 如何在批次檔(Batch)中實現 sleep 命令讓任務暫停執行 n 秒
author: wiloon
type: post
date: 2013-04-17T12:40:36+00:00
url: /?p=5406
categories:
  - Windows
tags:
  - Windows

---
在批次檔(*.bat)中內建並沒有 SLEEP 命令，當你在執行批次任務時若需要暫停執行幾秒鐘，就需要一些小技巧來實現了，以下分享幾個我之前用過的技巧：

**1. 利用 PING 指令幫忙停 5 秒**

每壹台電腦都有 PING 執行檔，這個最好用啦!


  @ping 127.0.0.1 -n 5 -w 1000 &gt; nul


**2. 利用 CHOICE 指令**

CHOICE 命令在 Windows XP 中找不到，但在 Windows Server 2003 或 Vista 都有內建。


  @CHOICE /C YN /N /T 5 /D y &gt; nul




**3. 安裝 **<a href="http://www.microsoft.com/Downloads/details.aspx?FamilyID=9d467a69-57ff-4ae7-96ee-b18c4790cffd&displaylang=en" target="_blank" rel="nofollow">Windows Server 2003 Resource Kit Tools</a>** 即可獲得 sleep.exe 工具**

預設安裝路徑在 **C:Program FilesWindows Resource KitsTools** 目錄下會有個 sleep.exe 執行檔


  sleep 5


**4. 利用 TIMEOUT 指令**

TIMEOUT 命令在 Windows Server 2003 或 Vista 之後都有內建。


  timeout /t 5
<a href="http://blog.miniasp.com/post/2009/06/24/Sleep-command-in-Batch.aspx">http://blog.miniasp.com/post/2009/06/24/Sleep-command-in-Batch.aspx</a>
