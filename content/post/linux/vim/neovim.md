---
title: "neovim"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "neovim"

http://liaoph.com/modern-vim/

Neovim 与 vim 的恩怨情仇
2014 年,巴西程序员 Thiago de Arruda Padilha (aka tarruda) 因为多次对 vim 提交 feature patch 遭到拒绝。出于对 vim 低效的开发社区的不满,决定众筹一个新项目 —— neovim,尝试解决 vim 当时的问题: 

由于 vim 写于 90 年代,20 多年过去,产生了大量的遗留代码,导致程序维护困难
社区新功能开发进度缓慢,vim 开发社区仍然使用邮件 patch 的方式协作,并且对新人极度不友好
作者 Bram Moolenaar 被形容为 vim 社区的独裁者,大量开发者提交的 patch 被拒绝
Neovim 项目发起之初,并不被人们看好,并且被认为是在重复造轮子。vim 作者 Bram 这样评价刚发起的 neovim 项目: 

It’s going to be an awful lot of work, with the result that not all systems will be supported, new bugs introduced and what’s the gain for the end user exactly?

但是随着时间的推移,neovim 项目逐渐发展成为一个成熟的项目,并率先提供了多个当时 vim 不支持的新特性: 

remote plugin,支持使用 python 等第三方语言编写的程序与 nvim 交互,开发插件
为 vimscript 提供了异步任务的支持,在此之前 vimscirpt 只能以同步的方式工作,任务卡住会导致 vim 前台卡住
支持在 vim 中打开 terminal window
重构了 vim 的部分代码,如使用 libuv 库来做多平台兼容,而不是像 vim 那样手动维护,并且使用更加现代化的代码编译工具链
neovim 项目的成功也激发了 bram 对 vim 项目开发的激情,促使 vim 在 7.0 之后极大的加快了新功能开发进度,很快发布了 vim8.0/8.1,把 neovim 实现的大部分新特性在 vim 中也实现了一遍。vim 现在也支持异步任务,terminal 等特性了。所以目前来看 neovim 与 vim 的差异已经很小,大部分第三方插件都能兼容 nvim/vim。

但是在这里还是强烈推荐使用 neovim: 

我从 neovim 0.17 版本开始使用 (macOS) ,使用下来,nvim 的稳定性和 vim 基本相当
neovim 始终保持先进性,由于社区开发进度更高效,各种新功能仍然还是先在 neovim 中实现,vim 才会有对应实现,并且现在 neovim 还被 google summer of code 支持,为其添加新特性
neovim 还有一些未被 vim 实现的特性,例如 Remote plugin, virtual text 等..

https://jdhao.github.io/2020/01/12/vim_nvim_history_development/
