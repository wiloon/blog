---
title: Moving The Ctrl Key
author: "-"
date: 2012-04-23T05:13:04+00:00
url: /?p=3011
categories:
  - Emacs

tags:
  - reprint
---
## Moving The Ctrl Key
>http://emacswiki.org/emacs/MovingTheCtrlKey

## Microsoft Windows {#toc15}

### AutoHotkey
On Windows you can use the [AutoHotkey][1] program which uses "scripts" to remap the keyboard.

This method has a couple benefits. One is scripts can be compiled to a stand alone .exe file which can be executed on a machine that doesn't have AutoHotkey. Another is, the key re-mapping can be set to only apply in emacs; the caps lock key will behave normaly in every other program. (If that's what you want.)

To remap the Caps Lock key to Ctrl save the following to a file named script.ahk. Then execute the script with [AutoHotKey][2] by double clicking it. See the [AHK2EXE][3]documentation to learn how to make scripts into stand alone executables.

#IfWinActive emacs  ; if in emacs
    +Capslock::Capslock ; make shift+Caps-Lock the Caps Lock toggle
    Capslock::Control   ; make Caps Lock the control button
    #IfWinActive        ; end if in emacs

The original Caps Lock behavior is here mapped to Shift + Caps Lock.

If you want the caps lock to be the control key everywhere remove the lines that begin with "#IfWinActive ".

http://www.emacswiki.org/emacs?action=edit;id=IfWinActive

If you want this AHK script to remain in effect across windows restarts place the script in your startup folder. See the [startup section of the AHK FAQ][4] for more specific directions.

 [1]: http://www.autohotkey.com/
 [2]: http://www.emacswiki.org/emacs/AutoHotKey
 [3]: http://autohotkey.free.fr/docs/Scripts.htm#ahk2exe
 [4]: http://www.autohotkey.com/docs/FAQ.htm#Startup