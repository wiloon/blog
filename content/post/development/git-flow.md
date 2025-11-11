---
title: git flow, Git 分支管理, github flow, gitlab flow
author: "-"
date: 2013-01-20T09:25:18+00:00
url: git-flow
categories:
  - Git
tags:
  - reprint
  - r3emix
  - Git
  - todo
---
## git flow, Git 分支管理, github flow, gitlab flow

### git flow

- main: 稳定的生产代码，只有发布版本才合并到这里, 长期分支，始终存在。
- develop：日常开发的主分支，所有新功能和 bug 修复先合并到 develop, 长期分支，始终存在。用于整合开发中的代码
- feature/xxx：新功能开发的临时分支，开发完成后合并到 develop, 合并之后删掉, 短期分支， 不是长期保持。开发新特性时创建,合并后删除
- release/xxx：发布准备分支，从 develop 分出，准备发布, 短期分支， 不是长期保持。
- hotfix/xxx：生产环境紧急修复，从 main 分出，修复后合并回 main 和 develop, 短期分支， 不是长期保持。

Git flow 是一个Git分支管理模型，由 Vincent Driessen 于2010年发布在其个人网站的一篇博文中《A successful Git branching model》，该模型适用于多版本管理的项目，能够有效的促进团队成员之间的协作，提升代码的清晰度。

https://nvie.com/posts/a-successful-git-branching-model/
https://www.cnblogs.com/youbins/p/17632165.html

Git flow的优点是清晰可控，缺点是相对复杂，需要同时维护两个长期分支。大多数工具都将master当作默认分支，可是开发是在develop分支进行的，这导致经常要切换分支，非常烦人。

更大问题在于，这个模式是基于”版本发布”的，目标是一段时间以后产出一个新版本。但是，很多网站项目是”持续发布”，代码一有变动，就部署一次。这时，master分支和develop分支的差别不大，没必要维护两个长期分支。

### github flow

- 只有主分支（通常是 main 或 master）和临时 feature 分支。
- 在 GitHub Flow 中并不推荐或保留 develop 分支。
- feature/bugfix 分支：开发新功能或修复 bug 时，从 main 分出，开发完成后提 Pull Request（PR），通过代码审查后合并到 main。开发完成后通过 Pull Request 合并到 main，feature 分支随即删除。
- GitHub Flow 本身不适合多版本并行维护

https://docs.github.com/en/get-started/using-github/github-flow

Github flow 是Git flow的简化版，专门配合”持续发布”。它是 Github.com 使用的工作流程。

Github flow 的最大优点就是简单，对于”持续发布”的产品，可以说是最合适的流程。

问题在于它的假设：master分支的更新与产品的发布是一致的。也就是说，master分支的最新代码，默认就是当前的线上代码。

可是，有些时候并非如此，代码合并进入master分支，并不代表它就能立刻发布。比如，苹果商店的APP提交审核以后，等一段时间才能上架。这时，如果还有新的代码提交，master分支就会与刚发布的版本不一致。另一个例子是，有些公司有发布窗口，只有指定时间才能发布，这也会导致线上版本落后于master分支。

上面这种情况，只有master一个主分支就不够用了。通常，你不得不在master分支以外，另外新建一个production分支跟踪线上版本。

### gitlab flow

https://www.ruanyifeng.com/blog/2015/12/git-workflow.html

https://about.gitlab.com/blog/gitlab-flow-duo/

Gitlab flow 是 Git flow 与 Github flow 的综合。它吸取了两者的优点，既有适应不同开发环境的弹性，又有单一主分支的简单和便利。它是 Gitlab.com 推荐的做法。
它只有一个长期分支，就是main，因此用起来非常简单。

上游优先, Gitlab flow 的最大原则叫做”上游优先”（upsteam first），即只存在一个主分支 main, 它是所有其他分支的”上游”。只有上游分支采纳的代码变化，才能应用到其他分支。

对于”持续发布”的项目，它建议在main分支以外，再建立不同的环境分支。比如，”开发环境”的分支是main，”预发环境”的分支是pre-production，”生产环境”的分支是production。

开发分支是预发分支的”上游”，预发分支又是生产分支的”上游”。代码的变化，必须由”上游”向”下游”发展。比如，生产环境出现了bug，这时就要新建一个功能分支，先把它合并到main，确认没有问题，再cherry-pick到pre-production，这一步也没有问题，才进入production。

只有紧急情况，才允许跳过上游，直接合并到下游分支。

GitLab Flow 的灵活性
GitLab Flow 并不是一种“固定的分支模型”，而是一套分支管理思想和实践建议，它允许团队根据实际需求灵活选择分支策略。
官方文档明确提出，GitLab Flow 可以结合发布驱动（Release-based）、环境驱动（Environment-based）、功能驱动（Feature-based）等多种模式[1]。

----

https://cloud.tencent.com/developer/article/1646937

Vincent Driessen 提出了一个分支管理的策略，我觉得非常值得借鉴。它可以使得版本库的演进保持简洁，主干清晰，各个分支各司其职、井井有条。
理论上，这些策略对所有的版本管理系统都适用，Git只是用来举例而已。如果你不熟悉Git，跳过举例部分就可以了。

## 主分支 master/main

首先，代码库应该有一个、且仅有一个主分支。所有提供给用户使用的正式版本，都在这个主分支上发布。

Git主分支的名字，默认叫做 main。它是自动建立的，版本库初始化以后，默认就是在主分支在进行开发。

## 开发分支 develop

主分支只用来分布重大版本，日常开发应该在另一条分支上完成。我们把开发用的分支，叫做 develop。

这个分支可以用来生成代码的最新隔夜版本 (nightly) 。如果想正式对外发布，就在 main 分支上，对 develop 分支进行"合并" (merge) 。

Git创建 develop 分支的命令:

git switch -b develop main

将 develop 分支发布到 main 分支的命令:

## 切换到 main 分支

>git switch main

## 对 develop 分支进行合并

```bash
git merge develop
```

## 临时分支

前面讲到版本库的两条主要分支: Master和Develop。前者用于正式发布，后者用于日常开发。其实，常设分支只需要这两条就够了，不需要其他了。

但是，除了常设分支以外，还有一些临时性分支，用于应对一些特定目的的版本开发。临时性分支主要有三种:

> * 功能 (feature) 分支
> * 预发布 (release) 分支
> * 修补bug (fixbug) 分支

这三种分支都属于临时性需要，使用完以后，应该删除，使得代码库的常设分支始终只有Master和Develop。

## 功能分支

接下来，一个个来看这三种"临时性分支"。

第一种是功能分支，它是为了开发某种特定功能，从Develop分支上面分出来的。开发完成后，要再并入Develop。

功能分支的名字，可以采用feature-*的形式命名。

创建一个功能分支:

> git switch -b feature-x develop

开发完成后，将功能分支合并到develop分支:

> git switch develop
> git merge feature-x

删除feature分支:

> git branch -d feature-x

## 预发布分支

第二种是预发布分支，它是指发布正式版本之前 (即合并到Master分支之前) ，我们可能需要有一个预发布的版本进行测试。

预发布分支是从Develop分支上面分出来的，预发布结束以后，必须合并进Develop和Master分支。它的命名，可以采用release-*的形式。

创建一个预发布分支:

> git switch -b release-1.2 develop

确认没有问题后，合并到master分支:

> git switch master
> git merge release-1.2
> 对合并生成的新节点，做一个标签
> git tag -a 1.2

再合并到develop分支:

> git switch develop
> git merge release-1.2

最后，删除预发布分支:

> git branch -d release-1.2

## 修补bug分支

最后一种是修补bug分支。软件正式发布以后，难免会出现bug。这时就需要创建一个分支，进行bug修补。

修补bug分支是从Master分支上面分出来的。修补结束以后，再合并进Master和Develop分支。它的命名，可以采用fixbug-*的形式。

创建一个修补bug分支:

> git switch -b fixbug-0.1 master

修补结束后，合并到master分支:

> git switch master
> git merge fixbug-0.1
> git tag -a 0.1.1

再合并到develop分支:

> git switch develop
> git merge fixbug-0.1

最后，删除"修补bug分支"

> git branch -d fixbug-0.1

阮一峰 -- Git 工作流程

https://www.ruanyifeng.com/blog/2015/12/git-workflow.html

gitlab flow



github flow



https://gitlab.com/gitlab-org/gitlab-foss/-/blob/0fdb03ee16f0ccd7f122a4f0af23ee628d1de3c9/doc/workflow/gitlab_flow.md
