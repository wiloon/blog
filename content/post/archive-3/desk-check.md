---
title: Desk Check
author: "-"
date: 2019-08-02T05:17:38+00:00
url: /?p=14759
categories:
  - Inbox
tags:
  - reprint
---
## Desk Check

  
    敏捷实践之Desk Check
  


http://insights.thoughtworkers.org/desk-check/embed/#?secret=5PpVVMPtJf

开发人员在完成需求之后，快速在本地开发环境建立功能验证条件。

开发人员要做的具体工作是: 需要测试数据的，建立mock data；然后对照Acceptance Criteria给团队的BA、QA展示完成的功能。这里需要注意的是，开发人员最好自己先完成一遍测试。自测能够发现一些问题，提高deskcheck的成功率，也吻合越早发现问题修复的代价越小的原理，否则不但耽误了自己的时间也耽误了BA和QA的时间。

BA的职责是: 验证开发之前提出的需求是否实现，是否有跟开发人员理解不一致的地方，是否有遗漏的需求。

QA的职责是: 从测试人员的视角评估这个功能有没有"ready for testing"，并且做一个快速的测试，验证是否有Sad Path没有考虑周全。

不管怎么说Desk Check还是处于developing的阶段，在这个阶段矫正一下需求，修复一些快速的defects，这样才能让功能ready进入下一个阶段: 测试环境的测试。

之前一直错误地理解Desk Check是我们开发流程的一部分，是流程上的一个要求。但是结合最近项目的实践和敏捷宣言的理论，意识到Desk Check实际上是践行了宣言的第一条: 个体之间的合作，而且合作比流程更重要。Desk Check同时也体现了反馈在敏捷开发中的作用，及时的反馈能够尽早的纠正工作的偏差，让我们一直向正确的方向前进。

https://www.techwalla.com/articles/what-is-desk-checking