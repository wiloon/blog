---
title: mariaDB
author: "-"
date: 2013-06-14T15:06:04+00:00
url: /?p=5538
categories:
  - DataBase
tags:
  - reprint
---
## mariaDB

  个向后兼容、替代MySQL的数据库服务器。它包含所有主要的开源存储引擎。

    为何改了个名字呢，这其中是有些典故的。
  
  
    MySQL之父Widenius先生离开了Sun之后，觉得依靠Sun/Oracle来发展MySQL，实在很不靠谱，于是决定另开分支，这个分支的名字叫做MariaDB。
  
  
    MariaDB跟MySQL在绝大多数方面是兼容的，对于开发者来说，几乎感觉不到任何不同。目前MariaDB是发展最快的MySQL分支版本，新版本发布速度已经超过了Oracle官方的MySQL版本。
  
  
    在Oracle控制下的MySQL开发，有两个主要问题: 1. MySQL核心开发团队是封闭的，完全没有Oracle之外的成员参加。很多高手即使有心做贡献，也没办法做到。2. MySQL新版本的发布速度，在Oracle收购Sun之后大为减缓。Widenius有一个ppt，用数据比较了收购之前和之后新版本的发布速度。有很多bugfix和新的feature，都没有及时加入到发布版本之中。
  
  
    以上这两个问题，导致了各个大公司，都开发了自己定制的MySQL版本，包括Yahoo!/Facebook/Google/阿里巴巴+淘宝网等等。
  
  
    MySQL是开源社区的资产，任何个人/组织都无权据为己有。为了依靠广大MySQL社区的力量来更快速的发展MySQL，另外开分支是必须的。
  
  
    MariaDB默认的存储引擎是Maria，不是MyISAM。Aria可以支持事务，但是默认情况下没有打开事务支持，因为事务支持对性能会有影响。可以通过以下语句，转换为支持事务的Aria引擎。ALTER TABLEtablenameENGINE=MARIATRANSACTIONAL=1;
  
  
    MariaDB源代码公开存放于Launchpad项目托管平台，同时也提供了二进制和编译包供下载。MariaDB基于事务的Maria存储引擎，替换了MySQL的MyISAM存储引擎，它使用了Percona的 XtraDB，InnoDB的变体，分支的开发者希望提供访问即将到来的MySQL 5.4 InnoDB性能。这个版本还包括了 PrimeBase XT (PBXT) 和 FederatedX存储引擎。
  