---
title: Enable Or Disable Hibernate Option In Windows 7
author: wiloon
type: post
date: 2014-03-08T05:04:19+00:00
url: /?p=6368
categories:
  - Uncategorized
tags:
  - Windows

---
http://www.intowindows.com/how-to-enable-hibernate-option-in-windows-7/

In Windows XP enabling Hibernate option was a very easy task. One could navigate to Control Panel, Power Options and then Hibernate tab to enable or disable Hibernation feature. But in Windows 7, we have to follow a different approach to do the same job.

&nbsp;

If you are not aware of Hibernate feature, Hibernation is a power-saving state designed primarily for laptops. While sleep puts your work and settings in memory and draws a small amount of power, hibernation puts your open documents and programs on your hard disk and then turns off your computer. Of all the power-saving states in Windows, hibernation uses the least amount of power. On a laptop, use hibernation when you know that you won’t use your laptop for an extended period and won’t have an opportunity to charge the battery during that time.

&nbsp;

Hibernate option in windows 7

&nbsp;

So if you are really going to use this feature then you need to enable it by doing a simple procedure as mentioned below:

&nbsp;

Step 1: Open Command Prompt with Administrator rights. To open Command Prompt, type CMD in Start menu and then hit Ctrl + Shift + Enter to open the Command Prompt with Admin rights.

&nbsp;

Step 2: Next, type the below command and hit enter:

&nbsp;

powercfg /hibernate on

&nbsp;

Hibernate command

&nbsp;

Step 3: Type exit and hit enter to close the Command Prompt.

&nbsp;

Step 4: If you can’t see the Hibernate option in Start menu then continue with the following tasks:

&nbsp;

A. Type Power Options in Start menu and hit enter.

&nbsp;

B. In the left pane, open the link labeled “Change when the computer sleeps” and then open the link “Change advanced power settings”.

&nbsp;

Hybrid sleep

&nbsp;

C. Under the Advanced Sleep options, expand the Sleep tree and turn off Hybrid Sleep.

&nbsp;

D. Now go back to Start menu to see the new Hibernate entry. That’s it!