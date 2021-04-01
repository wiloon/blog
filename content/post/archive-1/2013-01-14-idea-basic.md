---
title: idea basic, command
author: w1100n
type: post
date: 2013-01-14T07:37:05+00:00
url: /?p=5018
categories:
  - Java

---
### settings repository
    mkdir local-jetbrain-setting-repo
    cd local-jetbrain-setting-repo
    git init --bare
    # configure IntelliJ to save settings to git repo URL: "/path/to/local-jetbrain-setting-repo"
    git remote add origin git@github.com:wiloon/jetbrain-idea-setting.git
    git push origin master

### fetch
    git fetch origin master


### keys
|||
|-|-|
|列编辑|Alt+Shift+Insert,ctrl+alt+i |
|Expand All|Ctrl+Shift+= |

CTRL+SHIFT+N 查找文件
  
duplicate line and block
  
ctl+alt+Y sychronize
  
ctl+alt+S setting

---

### settings repository
    mkdir local-jetbrain-setting-repo
    cd local-jetbrain-setting-repo
    git init --bare
    # configure IntelliJ to save settings to git repo URL: "/path/to/local-jetbrain-setting-repo"
    git branch -m main # 默认创建
    git remote add origin git@github.com:wiloon/jetbrain-idea-setting.git
    git push origin main