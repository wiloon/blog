---
title: keepassxc
author: "-"
date: 2018-06-19T02:49:32+00:00
url: keepassxc
categories:
  - inbox
tags:
  - reprint
---
## keepassxc

### win10

#### install win32 openssh

    https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH

download and install openssh, OpenSSH-Win64.zip

    https://github.com/PowerShell/Win32-OpenSSH/releases/

#### install

powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
net start sshd
Set-Service sshd -StartupType Automatic

<https://github.com/rupor-github/wsl-ssh-agent>
<https://github.com/jstarks/npiperelay>  
<https://blog.wiloon.com/?p=13028&embed=true#?secret=RVVrbehtY9>
  
<https://keepassxc.org/>
