---
title: "hugo, envoy, github actions"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "hugo, envoy, github actions"

### install

```bash
    sudo pacman -S hugo

    hugo new site quickstart
    cd quickstart
    git init
    git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
    echo theme = \"ananke\" >> config.toml
    hugo new posts/my-first-post.md
    hugo server -D


    hugo new site wiloon.com
    cd wiloon.com
    git init
    git clone https://github.com/olOwOlo/hugo-theme-even themes/even
    cp themes/even/exampleSite/config.toml   config.toml 
    hugo new post/my-first-post.md
    hugo server -D
```

### hugo pages, nginx server simple

```bash
    podman run -d \
    --name hugo   \
    -p 30080:80 \
    -v /home/blog/public:/usr/share/nginx/html   \
    -v /etc/localtime:/etc/localtime   \
    nginx:alpine
```

### hugo pages, nginx server

```bash
    podman run -d \
    --name hugo   \
    --ip=10.88.0.10   \
    -v /home/blog/public:/usr/share/nginx/html   \
    -v /etc/localtime:/etc/localtime   \
    nginx:alpine
```

### hugo-envoy

```bash
    podman run -d \
    --name hugo-envoy   \
    -v /opt/hugo/service-envoy.yaml:/etc/envoy/envoy.yaml   \
    -v /etc/localtime:/etc/localtime   \
    --net=container:hugo \
    envoyproxy/envoy-alpine:v1.14.1
```

### front-envoy

```bash
    podman run -d \
    --name front-envoy \
    --add-host=hugo:10.88.0.10 \
    -v /opt/hugo/front-envoy.yaml:/etc/envoy/envoy.yaml \
    -v /etc/localtime:/etc/localtime \
    -v /root/.acme.sh/yangcs.net:/root/.acme.sh/yangcs.net \
    --net host \
    envoyproxy/envoy-alpine:v1.14.1
```

[https://blog.humblepg.com/post/2020/02/log-hugo-github-actions.html](https://blog.humblepg.com/post/2020/02/log-hugo-github-actions.html "https://blog.humblepg.com/post/2020/02/log-hugo-github-actions.html")

一、设置密钥

生成密钥

```bash
    ssh-keygen -t rsa -b 4096 -C "$(git config user.email)" -f gh-pages -N ""
```

得到 `gh-pages` 和 `gh-pages.pub` 两个文件

打开 GitHub 上 Hugo 项目代码库的 Setting 页面

* `Deploy keys` > `Add deploy key`，把文件 `gh-pages.pub` 的内容填入，勾选 `Allow write access`
* `Secrets` > `Add a new secret`，Name 为 `ACTIONS_DEPLOY_KEY`，Value 为文件 `gh-pages` 的内容

## 二、添加配置文件

在 Hugo 项目该位置添加配置文件: `.github/workflows/gh-pages.yml`

文件内容照抄 [GitHub Actions for Hugo](https://github.com/peaceiris/actions-hugo)

    name: github pages
    
    on:
      push:
        branches:
          - master
    
    jobs:
      build-deploy:
        runs-on: ubuntu-18.04
        steps:
          - uses: actions/checkout@v1  # v2 does not have submodules option now
            # with:
            #   submodules: true
    
          - name: Setup Hugo
            uses: peaceiris/actions-hugo@v2
            with:
              hugo-version: '0.62.2'
              # extended: true
    
          - name: Build
            run: hugo --minify
    
          - name: Deploy
            uses: peaceiris/actions-gh-pages@v3
            with:
              deploy_key: ${{ secrets.ACTIONS_DEPLOY_KEY }}
              publish_dir: ./public

这个 Workflow 一目了然

1. 当推送到 master 分支时触发
2. 运行 ubuntu
3. 调用 checkout action 获取源代码
4. 调用 hugo action 配置 Hugo
5. 运行 Hugo 生成网站内容
6. 调用 gh-pages action 把 `./public` 目录下的内容提交到 gh-pages 分支

虽然自己定制还需要学习，但常见的自动化任务把别人写好的配置文件拿来用是很简单的。

## 三、运行

把 Workflow 文件提交、推送即可触发，Hugo 站点发布到 GitHub Pages。以后每次推送都会触发，以实现 Hugo 站点的自动发布。

### script, blog-new.sh

```bash
#!/bin/sh

title=$1
f=${title// /-}
touch /home/wiloon/projects/wiloon.com/content/post/inbox/$f.md
d=`date '+%Y-%m-%d %H:%M:%S'`
cat <<EOF > /home/wiloon/projects/wiloon.com/content/post/inbox/$f.md
---
title: "$title"
author: "-"
date: "$d"
url: "$f"
categories:
  - inbox
tags:
  - inbox
---
## "$title"
EOF
```
