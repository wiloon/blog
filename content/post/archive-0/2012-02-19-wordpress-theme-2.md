---
title: wordpress theme
author: "-"
type: post
date: 2012-02-19T09:10:27+00:00
url: /?p=2352
categories:
  - Uncategorized

---
home.php和index.php，WordPress程序会从你的主题文件夹中依次查找这两个文件，如果找到home.php，则使用home.php作为博客首页模板，即使你的主题文件夹中有index.php；如果home.php未找到，则使用index.php作为首页模板；如果home.php和index.php都找不到，你的主题将不会被WordPress识别，等于废物。

**主页：**

  1. home.php
  2. index.php

**文章页：**

  1. single-{post_type}.php – 如果文章类型是videos（即视频），WordPress就会去查找single-videos.php（WordPress 3.0及以上版本支持）
  2. single.php
  3. index.php