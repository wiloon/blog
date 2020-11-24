---
title: keepassxc
author: w1100n
type: post
date: 2018-06-19T02:49:32+00:00
url: /?p=12319
categories:
  - Uncategorized

---
# keepassxc
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
    <a href="https://blog.wiloon.com/?p=13028">systemd/User ssh-agent</a>

https://github.com/rupor-github/wsl-ssh-agent
https://github.com/jstarks/npiperelay  
https://blog.wiloon.com/?p=13028&embed=true#?secret=RVVrbehtY9
  
https://keepassxc.org/
