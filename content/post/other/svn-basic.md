---
title: svn basic, command
author: "-"
date: 2011-08-04T02:41:54+00:00
url: svn
categories:
  - inbox
tags:
  - reprint
---
## svn basic, command
### ignore ca
    --trust-server-cert-failures="unknown-ca,cn-mismatch,expired,not-yet-valid,other"
    svn checkout https://your.repository.url/ --non-interactive --trust-server-cert-failures="unknown-ca,cn-mismatch,expired,not-yet-valid,other" --username=blah --password=blah
    
### 查看 svn 版本
    svn --version

### svn merge

```bash
# 分支合到主干 cd trunk
svn merge -r <revision where branch was cut>:<revision of trunk> svn://branch/path

# 分支当前版本为4847，想把4825到4847间的改动merge到主干
# cd trunk
svn merge -r 4825:4847 svn://branch/path
svn ci -m "merge branch changes r4835:4847 into trunk"

# 主干合到分支 cd branch
# 在r23创建了一个分支，trunk版本号更新到了25，想把23-25之间的改动merge到分支
svn merge -r 23:25 svn://trunk/path
svn ci -m "merge trunk changes r23:25 into my branch"

# cd trunk
# 查看当前Branch中已经有那些改动已经被合并到Trunk中
svn mergeinfo svn://branch/path

# cd trunk
# 查看Branch中那些改动还未合并
svn merginfo svn://branch/path --show-revs eligible
```

```bash
svn cat -- 显示特定版本的某文件内容。

svn list -- 显示一个目录或某一版本存在的文件列表。
svn list -v http://svn.test.com/svn  #查看详细的目录的信息(修订人,版本号,文件大小等)。
svn log -- 显示svn 的版本log，含作者、日期、路径等。

svn diff -- 显示特定修改的行级详细信息。
```

### resolve

```bash
svn resolve --accept working 1.txt
svn resolve --accept theirs-full 1.txt 使用1.txt.rNew作为最后提交的版本
svn resolve --accept mine-full 1.txt 使用1.txt.mine作为最后提交的版本
svn resolve --accept mine-conflict 1.txt 使用1.txt.mine的冲突部分作为最后提交的版本
svn resolve --accept theirs-conflict 1.txt 使用1.txt.rNew的冲突部分作为最后提交的版本
```

```bash
# 查看远程地址
svn info

# checkout
svn checkout  --username user0 http://路径(目录或文件的全路径)[本地目录全路径]

#查看目录状态
svn status
svn status -u

# checkout 指定版本
svn up -rXXXX

#install
yum install subversion

svn checkout https://(项目名称).(域)/svn/(项目名称)/(DIR) (项目名称) --username [在此处输入用户名]
svn update

#更新到指定版本
svn up -r xxx

# 如果出现 an unversioned directory of the same name already exists， 可以使用强制更新
#强制更新
svn up --force

svn commit -m 'xxx'

svn revert .

svn delete --force foo

svn revert foo

svn propedit svn:ignore .

svn propset svn:ignore dirname .

None of the environment variables SVN_EDITOR,
export SVN_EDITOR=vim
```

cd /home/wiloon/tmp
  
svn checkout file:///usr/xxx/data/xxx/meprepo/repos/

svn add FILENAME/DIR
  
cd repos
  
svn log -v

https://www.kancloud.cn/i281151/svn/197097
  
http://my.oschina.net/shelllife/blog/142257
  
http://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.revert.html
  
http://riaoo.com/subpages/svn_cmd_reference.html#commit
  
http://riaoo.com/subpages/svn_cmd_reference.html
  
https://www.cnblogs.com/zhenjing/archive/2012/12/22/svn_usage.html