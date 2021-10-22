---
title: keepassxc
author: "-"
type: post
date: 2018-06-19T02:49:32+00:00
url: /?p=12319


---
## keepassxc
### win10
#### install win32 openssh
    https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH
#### download and install openssh, OpenSSH-Win64.zip
    https://github.com/PowerShell/Win32-OpenSSH/releases/

#### install 
powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
net start sshd
Set-Service sshd -StartupType Automatic

### 启用openssh authentication agent
计算机管理>服务>openssh authentication agent > 启动>启动类型>自动 

### win10, wsl2, keepassxc
修改sshd 配置/etc/ssh/ssh_config, 开启转发

    ForwardAgent yes
    # 重启sshd生效
    systemctl restart sshd

修改~/.zshrc

    export SSH_AUTH_SOCK=$HOME/.ssh/agent.sock
    ss -a | grep -q $SSH_AUTH_SOCK
    if [ $? -ne 0   ]; then
                rm -f $SSH_AUTH_SOCK
                    ( setsid socat UNIX-LISTEN:$SSH_AUTH_SOCK,fork EXEC:"/mnt/d/workspace/apps/npiperelay.exe -ei -s //./pipe/openssh-ssh-agent",nofork & ) >/dev/null 2>&1
    fi


### systemd user service
>wangyue.dev/ssh-agent


https://github.com/rupor-github/wsl-ssh-agent
https://github.com/jstarks/npiperelay  
https://blog.wiloon.com/?p=13028&embed=true#?secret=RVVrbehtY9
  
https://keepassxc.org/
