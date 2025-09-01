---
title: nerdctl
author: "-"
date: 2025-09-01 14:31:02
url: nerdctl
categories:
  - Container
tags:
  - reprint
  - remix

---
## nerdctl

```bash
# nerdctl update 命令来修改容器的配置，包括重启策略。
sudo nerdctl update --restart unless-stopped kafka
# 验证
sudo nerdctl inspect kafka | grep -A 5 restart.policy
```
