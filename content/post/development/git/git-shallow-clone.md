---
title: "Git Shallow Clone 浅克隆与部分克隆"
author: "-"
date: 2026-10-02T08:47:04+08:00
lastmod: 2026-10-02T08:47:04+08:00
url: git/shallow-clone
categories:
  - Git
tags:
  - git
  - ci
  - remix
  - AI-assisted
---

## 为什么要用

`git clone` 默认会把整个历史的所有对象都拉下来。有些场景只需要最新的一份代码，甚至只需要其中一个文件，例如 CI 里构建镜像、流水线里改一行 GitOps manifest 的镜像 tag。这时完整克隆既慢又浪费，网络差的时候还可能超时。

Git 提供了三种互相独立、可以叠加的裁剪方式：

| 方式 | 参数 | 裁掉什么 |
| ---- | ---- | -------- |
| 浅克隆 shallow clone | `--depth N` | 历史：只要最近 N 个 commit |
| 部分克隆 partial clone | `--filter=blob:none` 等 | 文件内容：blob 用到时再按需下载 |
| 稀疏检出 sparse checkout | `--sparse` + `git sparse-checkout` | 工作区：只检出指定路径 |

## 浅克隆 --depth

```bash
# only the latest commit
git clone --depth 1 https://github.com/foo/bar.git

# --depth implies --single-branch; name the branch explicitly
git clone --depth 1 --branch main https://github.com/foo/bar.git

# by time instead of count
git clone --shallow-since=2026-01-01 https://github.com/foo/bar.git
```

`--depth` 默认带上 `--single-branch`，只拉一个分支。需要其它分支时，加 `--no-single-branch`。

浅克隆之后的常用操作：

```bash
# deepen history by 50 more commits
git fetch --deepen=50

# turn it into a full clone
git fetch --unshallow

# check whether the repo is shallow
git rev-parse --is-shallow-repository
```

`--depth 1` 只裁掉了历史。如果仓库当前版本本身就有大文件，比如提交进仓库的二进制或数据文件，体积还是下不来。

## 部分克隆 --filter

部分克隆会保留完整的 commit 和 tree，但是不预先下载文件内容（blob）。checkout、diff 等命令用到哪个 blob，再去服务器取哪个。服务端需要支持，GitHub、GitLab 都支持。

```bash
# no blobs up front; fetched on demand
git clone --filter=blob:none https://github.com/foo/bar.git

# skip blobs larger than 1 MB
git clone --filter=blob:limit=1m https://github.com/foo/bar.git

# no trees either (smallest, but many later commands trigger fetches)
git clone --filter=tree:0 https://github.com/foo/bar.git
```

和浅克隆不同，部分克隆后 `git log` 能看到完整历史，只是看文件内容时要联网。

## 稀疏检出 sparse checkout

只把需要的路径检出到工作区。和 `--filter=blob:none` 一起用时，没检出的文件不会下载内容。

```bash
git clone --filter=blob:none --sparse https://github.com/foo/bar.git
cd bar

# cone mode: whole directories
git sparse-checkout set docs src/api

# non-cone mode: exact file patterns
git sparse-checkout set --no-cone /k8s/app/deployment.yaml

# back to a full working tree
git sparse-checkout disable
```

## 三者叠加：只改一个文件

CI 里改 GitOps 仓库里某个 manifest 的镜像 tag，只需要一个文件，下面这条命令拉到的东西最少：

```bash
git clone --depth 1 --single-branch --branch main \
  --filter=blob:none --sparse git@github.com:foo/gitops.git gitops
cd gitops
git sparse-checkout set --no-cone /k8s/app/deployment.yaml
```

我在一个约 32 MB pack 的配置仓库上实测的 `.git` 大小（这个仓库当前版本里有几个 10–20 MB 的数据文件）：

| 方式 | `.git` 大小 |
| ---- | ----------- |
| 完整克隆 | 约 32 MB |
| `--depth 1` | 25 MB |
| `--filter=blob:none --no-checkout` | 876 KB |
| `--depth 1 --filter=blob:none --sparse` + 一个文件 | 332 KB |

可以看到，只用 `--depth 1` 效果有限，体积主要来自当前版本的大文件，要靠 `--filter` 才能省掉。

## 在浅克隆里提交和推送

在浅克隆里 `commit` 和 `push` 都可以正常用，push 不需要完整历史。

有个坑：push 被拒（`! [rejected] ... (fetch first)`）后，不能像平时那样 `fetch` 再 `rebase`。

```bash
git fetch --depth 1 origin main
git rebase origin/main   # conflicts
```

原因是 `--depth 1` 拉下来的新远端提交没有父提交，本地也就找不到它和自己分支的共同祖先。rebase 会把本地浅边界上那个旧提交也当成"自己的提交"重放一遍，结果产生冲突。先 `git fetch --unshallow` 再 rebase 可以解决，但这样又把完整历史拉回来了。

如果改动是幂等的（比如用 sed 把镜像 tag 替换成固定值），更简单的做法是丢掉本地提交，在远端最新版本上重做一遍：

```bash
update_and_commit() {
  sed -i "s|image:.*myapp.*|image: ${IMAGE}|" k8s/app/deployment.yaml
  git add k8s/app/deployment.yaml
  git commit -m "Update image to ${IMAGE}" || echo "No changes to commit"
}
update_and_commit

for attempt in 1 2 3 4 5; do
  git push origin HEAD:main && break
  [ "$attempt" -eq 5 ] && { echo "push failed" >&2; exit 1; }
  # rejected by a concurrent push: redo the edit on the new tip
  git fetch --depth 1 origin main
  git reset --hard FETCH_HEAD
  update_and_commit
  sleep $((attempt * 2))
done
```

## 相关

- [Git 常用命令](./commands.md)
- [Git Worktree](./git-worktree.md)
- [git-clone 文档](https://git-scm.com/docs/git-clone)
- [git-sparse-checkout 文档](https://git-scm.com/docs/git-sparse-checkout)
- [Partial clone 文档](https://git-scm.com/docs/partial-clone)
