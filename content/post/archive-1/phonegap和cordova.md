---
title: PhoneGap和Cordova
author: "-"
date: 2015-02-05T06:07:17+00:00
url: /?p=7313
categories:
  - Uncategorized

tags:
  - reprint
---
## PhoneGap和Cordova
http://www.smallhead.cn/knowledge/422.html

说到PhoneGap,大家会提到Cordova,这也是近期新手们经常谈论的问题,有的人直接问我你用的是PhoneGap还是Cordova？这里我说说我对这两个名字的理解。

谈着两个名字必须要涉及到两个名词的由来,也就是说说他们的历史。小头我从phonegap1.9版本一直沿用到现在发展的3.3版本,了解他的发展历史也有一点。

2008年8月,PhoneGap在旧金山举办的iPhoneDevCamp上崭露头角,起名为PhoneGap是创始人的想法: "为跨越Web技术和iPhone之间的鸿沟牵线搭桥"。当时PhoneGap隶属于Nitobe公司。经过几个版本的更新,这款PhoneGap开始支持更多的平台,在2011年10月4日,Adobe公司收购了这个Nitobe公司,当时adobe公司还有着adobe air 和flash。随后Adobe把PhoneGap项目捐献给了Apache基金会,但是保留了PhoneGap的商标所有权。而就在这时候PhoneGap开始分两条路而走,在Adobe公司内部一直保有着PhoneGap的商标所有权,而Apache收录这个项目后将其更名为Apache Callback。而捐献之后虽然PhoneGap的升级和维护工作大部分还是依托于Adobe的Nitobe项目组,所以在Adobe的PhoneGap官方宣扬的"PhoneGap"名号,而Apache对外公布的确实Callback名号,当2012年PhoneGap更新到1.4版本后,Apache又把名字更新成Cordova,有趣的是Cordova是PhoneGap团队附近一条街的名字。

随后就出现了我们经常混淆的PhoneGap和Cordova两个名字混淆的状况。从概念上将,两者的区别如下: 

  1. Cordova是Adobe捐献给Apache的项目,是一个开源的、核心的跨平台模块。而PhoneGap是Adobe的一项商业产品。
  2. Cordova和Phonegap的关系就类似于WebKit与Chrome或者Safari的关系。
  3. PhoneGap还包括一些额外的商用组件,例如PhoneGap Build和Adobe Shadow。

然而如果不从概念上讲,其实Adobe的PhoneGap产品和Apache的Cordova项目维护的是共同的一份源代码组件(现在是这个状况)。也就是说如果你问我使用Cordova还是PhoneGap,我只能说这两个东西我都在用 (而实质上我用的是一个东西,只不过两个名号而已) 。所以当我们使用PhoneGap开发的时候无论是Cordova和PhoneGap其实都一样,但是心理要明白,在概念上Phonegap其实是Cordova的个例产品,PhoneGap是基于Cordova之上的加上云端打包和Adobe Shadow的系列产品综合。就我个人理解,PhoneGap的范围大于Cordova。

以下是迷惑解答: 

1.Adobe公司为什么要捐献这个项目？

答: 其实在收购Nitobe公司的时候就已经做定主意将PhoneGap开源,具体原因也许只能是Adobe的高层才能解释,小头理解应该是当时的Adobe公司一直以收费软件来盈利,做一款公益的框架不是Adobe的作风,而当时Adobe Flash的挫败使得Adobe必须有一个时代的替代品,而PhoneGap就是这么一个产品,所以Adobe不准备在核心代码上做文章,而是通过收费的PhoneGap build和Adobe Shadow来占领市场,将PhoneGap开源能够保证框架的大面积推广,还有可以将这个项目的维护等工作渐渐推给Apache。

2.Apache为什么来回改名字？

答: 当初Apache收录该项目的时候由于PhoneGap的商标所有权还在Adobe公司,所以Apache不得不重新命名该项目,而apache的传统一般的将开源软件命名成根据作者的小物品或家乡名称,所以最终确定为cordova名称也情有可原。

3.PhoneGap会不会在Cordova之上建立私有代码？

答: 就目前官方博客给出的消息是,到现在为止Phonegap和Apache Cordova唯一的区别就是包的名字不同,而这种状态还是会持续一段时间,并且在"持续一段时间"上加重语气。所以暂时不用担心在代码上PhoneGap和Cordova的不同。

参考: 

《深入浅出PhoneGap》饶侠,张坚,赵丽萍编著

PhoneGap官方博客http://phonegap.com/2012/03/19/phonegap-cordova-and-what%E2%80%99s-in-a-name/

百度百科——Cordova