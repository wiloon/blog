---
title: vscode, Visual Studio Code, Visual Studio Code Server
author: wiloon
type: post
date: 2019-05-05T07:42:04+00:00
url: /?p=14288
categories:
  - Uncategorized

---
### plugin
#### Markdown All in One
    ctrl+shift+i - 表格格式化
#### Settings Sync
#### Github Markdown Preview

https://github.com/cdr/code-server

```bash
docker run \
-d \
--name vscode-server \
-p 8443:8443 \
-v /etc/localtime:/etc/localtime:ro \
-v vscode-projects:/home/coder/project \
--restart=always \
codercom/code-server \
--allow-http \
--no-auth

```