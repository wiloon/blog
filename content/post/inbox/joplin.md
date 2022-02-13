---
title: "joplin"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "joplin"

### archlinux

    yay -S joplin-desktop
#### direct install
    wget -O - https://raw.githubusercontent.com/laurent22/joplin/dev/Joplin_install_and_update.sh | bash
### vscode install joplin plugin
    安装 chrome 扩展: Joplin Web Clipper

### enable web clipper service
    joplin desktop > setting>web clipper > enable web clipper service

### vscode
打开vscode setting 搜索joplin, 填写 
#### joplin: Port
web clipper 端口， 
#### jplin路径 ，
 token，
  重启vscode 

## typora
打开Joplin，然后点击菜单栏的工具，在弹出的菜单中选择选项

Tools>Options>General>Text editor command>Path
填写typora 可执行文件的位置。

### docker server
>https://hub.docker.com/r/joplin/server
```bash
podman run --rm --name joplin --env-file /data/joplin.env -p 22300:22300 joplin/server:2.7.3-beta
podman run -d --name joplin --env-file /data/joplin.env -p 22300:22300 joplin/server:2.7.3-beta
```
### joplin.env
```
# =============================================================================
# PRODUCTION CONFIG EXAMPLE
# -----------------------------------------------------------------------------
# By default it will use SQLite, but that's mostly to test and evaluate the
# server. So you'll want to specify db connection settings to use Postgres.
# =============================================================================
#
# APP_BASE_URL=https://example.com/joplin
# APP_PORT=22300
#
# DB_CLIENT=pg
# POSTGRES_PASSWORD=joplin
# POSTGRES_DATABASE=joplin
# POSTGRES_USER=joplin
# POSTGRES_PORT=5432
# POSTGRES_HOST=localhost

# =============================================================================
# DEV CONFIG EXAMPLE
# -----------------------------------------------------------------------------
# Example of local config, for development. In dev mode, you would usually use
# SQLite so database settings are not needed.
# =============================================================================
#
APP_BASE_URL=http://192.168.50.13:22300
APP_PORT=22300
```


>https://github.com/laurent22/joplin
