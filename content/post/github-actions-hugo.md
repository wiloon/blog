+++
date = 2020-05-12T15:03:55Z
title = "github actions, hugo"

+++
[https://blog.humblepg.com/post/2020/02/log-hugo-github-actions.html](https://blog.humblepg.com/post/2020/02/log-hugo-github-actions.html "https://blog.humblepg.com/post/2020/02/log-hugo-github-actions.html")

一、设置密钥

生成密钥

    ssh-keygen -t rsa -b 4096 -C "$(git config user.email)" -f gh-pages -N ""
    

得到 `gh-pages` 和 `gh-pages.pub` 两个文件

打开 GitHub 上 Hugo 项目代码库的 Setting 页面

* `Deploy keys` > `Add deploy key`，把文件 `gh-pages.pub` 的内容填入，勾选 `Allow write access`
* `Secrets` > `Add a new secret`，Name 为 `ACTIONS_DEPLOY_KEY`，Value 为文件 `gh-pages` 的内容

## 二、添加配置文件

在 Hugo 项目该位置添加配置文件：`.github/workflows/gh-pages.yml`

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