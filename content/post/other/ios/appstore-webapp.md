---
title: 苹果 WebApp
author: "-"
date: 2015-01-12T08:09:18+00:00
url: /?p=7226
categories:
  - Inbox
tags:
  - reprint
---
## 苹果 WebApp

苹果真的要在 AppStore 里封杀 WebApp 吗?

[http://fins.iteye.com/blog/1685886](http://fins.iteye.com/blog/1685886)

  苹果真的要在 AppStore 里封杀 WebApp 吗 ?
  
    最近几个月, 苹果AppStore似乎加强了对WebApp的管控, 很多过去能上架的 使用WebApp+Native壳的应用陆陆续续的都被拒了.
  
  
    于是 很多人开始抛出了"苹果要封杀WebApp"/"苹果要像当初对待Flash一样对HTML5说不"一类的观点.
  
  
    作为一个HTML5开发人员 + 苹果产品用户, 我也想表达一下自己对这个问题的看法.
 我的观点不一定对 但是,即使我错了,也不能证明那些认为"苹果要封杀WebApp"的荒谬观点是正确的(好流氓 哈哈).
  
    先来看一看让广大HTML5/WebApp开发者 感动忧虑的那段苹果的原文吧:
  
  
    引用
  
  
    If you cannot – or choose not to – revise your app to be in compliance with the App Store Review Guidelines, you may wish to build an HTML5 web app instead. You can distribute web apps directly on your web site; the App Store does not accept or distribute web apps.
  
  
    简单说就是一句话: 如果你的应用是一个Webapp, 那么请以网页的形式发布你的产品就好了, 不要放到AppStore里, AppStore不接收WebApp.
  
  
    不管怎么看 我都看不出来"苹果要封杀WebApp"的意思, 更看不出有些人YY的"苹果因为担心HTML5太强大了抢了Native的市场"这种观点.
  
  
    相反 我觉得苹果是在引导WebApp用正确的方式去发行: 如果你的应用在网页里也能跑, 但你却非要放到AppStore里, 结果就是赚了钱还要分给苹果30%, 而且更新升级什么的还要走漫长的审核过程,何苦呢?
  
  
    在AppStore方面, 苹果是靠应用(注意,是应用,而不是和某种具体技术绑定的应用.只要是合法的 好的应用,受欢迎卖得多,苹果都能赚钱,苹果才不关心应用用的是什么技术呢)分成赚钱, 如果纯粹从经济目的出发, 苹果完全没必要把WebApp从他能赚钱的领域(AppStore应用)驱赶到他不能赚钱的领域(Web浏览器).
  
  
    所以 一个合法的应用被拒绝的原因笼统的说只有三点: 1 违规(调用不该调用的方法,做了危险的事情,山寨抄袭等等) 2 苹果觉得应用不够好 3 觉得放到AppStore里不合适.
  
  
    前两点不用说大家都懂, 而最后一点我想是大量WebApp被拒绝的一个主要原因: 完全没有使用或者没必要使用任何Native的技术,在网页里也能跑. 通常这种应用只是把AppStore当做一个发行渠道.
  
  
    我特意去AppStore上搜索了下, 其实存在大量的Phonegap封装的应用, 我挑了几个免费的下来,解包看了一下, 它们都使用到了Phonegap提供的一些只有native技术才能实现的功能, 我想这是他们能通过审核的一个很重要的原因之一.
  
  
    =========================
 还有朋友提出了这样一个观点:"app store的意义是维护苹果利益，webapp可以同时存在多个平台，就会降低apple独占的市场份额，直接影响利益。"
  
    我是非常不赞同这种观点的. 把Webapp同时存在于多个平台 和 apple的利益 挂钩, 显然是套用了当年iOS和Flash之间的故事. 但两者完全没有可比性.
  
  
    当年Flash是想在浏览器里跑, 而苹果驱逐了它.
 WebApp想进入AppStore , 苹果建议它去浏览器里跑.
  
    一个是驱逐, 一个是换个地方跑, 完全不一样.
 当然 你可以说, 以后HTML5足够强大了, 苹果也许也会把WebApp驱逐.
 这么久远的事情到底会不会发生 我不知道, 但是我觉得,如果HTML5真的强大到和Flash一样牛逼, 苹果大可选择把WebApp赶回AppStore的策略, 这样才满足利益最大化啊.
  
    另外 我希望这位朋友你不妨思考思考如下几个问题(会用到反问,但绝对没有不敬之意):
 1)如果你是苹果,难道你不希望从自己平台诞生的应用,能红遍全球吗?就像愤怒的小鸟一样成为一种现象.
 2)如果你是苹果,难道你不希望其他平台热门的应用能早日降临到自己的iOS上吗?
 3)你觉得在智能移动设备上, 走传统游戏主机那种"独占游戏"的路能走得通吗?你觉得"因为某某应用只有iPhone有安卓没有,所以我要买iPhone"这样的事情发生的几率很大吗?
  
    ====================
  
  
    越说越散了,  该收收尾了. 最后总结一下吧.
  
  
    我也承认, AppStore有很多过分的要求, 但是这些绝对不是针对HTML5和WebApp来的.
 (例如 禁止远程修改代码, 禁止绕过appstore直接内部更新版本等等)
 所以我们没有必要因为几个WebApp被拒就对HTML5在iOS平台上的未来感到担忧.
  
    iOS系统作为对HTML5支持最好的移动平台, 我们没有理由怀疑它对HTML5的态度.
 我想,苹果加强对AppStore内WebApp的管理力度, 根本原因只是为了保证AppStore的质量.
  
    当然在整个事件中,苹果也有做的不妥的地方, 他始终没有针对webapp/ Hybrid技术构建的应用提出一个具体的 有章可循的规则说明,给人一种"法无定法"的感觉.
 但是随着Hybrid技术和HTML5技术的发展, 我想 苹果会对这个问题慢慢重视起来.
  