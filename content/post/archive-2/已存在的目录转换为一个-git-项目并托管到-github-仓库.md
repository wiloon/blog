---
title: 已存在的目录转换为一个 GIT 项目并托管到 GITHUB 仓库
author: "-"
date: 2017-09-10T07:31:39+00:00
url: /?p=11158
categories:
  - Uncategorized

tags:
  - reprint
---
## 已存在的目录转换为一个 GIT 项目并托管到 GITHUB 仓库

```bash
  
git init
  
git add .
  
git commit -m "Initial commit"

#访问 GitHub, 创建一个新仓库
  
git remote add origin https://github.com/superRaytin/alipay-app-ui.git
  
#git push origin master
  
git push -u origin master -f
  
```

http://leonshi.com/2016/02/01/add-existing-project-to-github/
  
http://blog.csdn.net/shiren1118/article/details/7761203