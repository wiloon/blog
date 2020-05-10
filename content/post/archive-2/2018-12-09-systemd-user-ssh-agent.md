---
title: 'systemd/User  ssh-agent'
author: wiloon
type: post
date: 2018-12-09T14:53:48+00:00
url: /?p=13028
categories:
  - Uncategorized

---
Start ssh-agent with systemd user

<pre><code class="language-shell line-numbers">vim ~/.config/systemd/user/ssh-agent.service
[Unit]
Description=SSH key agent

[Service]
Type=simple
Environment=SSH_AUTH_SOCK=%t/ssh-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a $SSH_AUTH_SOCK

[Install]
WantedBy=default.target
</code></pre>

<pre><code class="language-shell line-numbers">vim  ~/.pam_environment
SSH_AUTH_SOCK DEFAULT="${XDG_RUNTIME_DIR}/ssh-agent.socket"

</code></pre>

<pre><code class="language-shell line-numbers"># Then enable or start the service.
systemctl --user enable ssh-agent
systemctl --user start ssh-agent
# 检查环境变量 SSH_AUTH_SOCK
env | fgrep SSH_
# 如果看不到SSH_AUTH_SOCK ， 重启再试一下 
</code></pre>

https://wiki.archlinux.org/index.php/Systemd/User
  
https://wiki.archlinux.org/index.php/SSH_keys