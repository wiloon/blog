---
title: win11 ssh agent
author: "-"
date: 2019-04-05T05:18:16+00:00
url: win11/ssh/agent
categories:
  - network
tags:
  - reprint
  - remix
---
## win11 ssh agent

[https://www.cnblogs.com/sparkdev/p/10166061.html]()
[https://davidaugustat.com/windows/windows-11-setup-ssh]()

- making sure that the OpenSSH client is installed

1. Settings -> Apps -> Optional Features
2. Scroll to “OpenSSH Client” and click on the item
3. If it shows an “Uninstall” button, then OpenSSH is already installed, and you can skip to the next section.

open Windows service, win + R "services.msc"

- Enabling the SSH Authentication Agent
  - scroll to “OpenSSH Authentication Agent” and set to Automatic Delayed Start
- Generating the SSH key

add private key into ssh-agent

```Bash
ssh-add C:\Users\user0\.ssh\id_ed25519
```

search service

## unable to start ssh-agent service, error :1058

启用 openssh agent

Computer Management> Services> OpenSSH Authentication Agent

[https://davidaugustat.com/windows/windows-11-setup-ssh](https://davidaugustat.com/windows/windows-11-setup-ssh)