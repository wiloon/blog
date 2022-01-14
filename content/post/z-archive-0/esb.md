---
title: ESB
author: "-"
date: 2012-05-10T13:55:37+00:00
url: esb
categories:
  - Development
tags:
  - deprecated

---

  ESB全称为Enterprise Service Bus，即企业服务总线。它是传统中间件技术与XML、Web服务等技术结合的产物。ESB提供了网络中最基本的连接中枢，是构筑企业神经系统的必要元素。ESB的出现改变了传统的软件架构，可以提供比传统中间件产品更为廉价的解决方案，同时它还可以消除不同应用之间的技术差异，让不同的应用服务器协调运作，实现了不同服务之间的通信与整合。从功能上看，ESB提供了事件驱动和文档导向的处理模式，以及分布式的运行管理机制，它支持基于内容的路由和过滤，具备了复杂数据的传输能力，并可以提供一系列的标准接口。


  
    一、ESB的五个基本功能: 
  
  
    1)服务的MetaData管理: 在总线范畴内对服务的注册命名及寻址进行管理。
  
  
    2)传输服务: 确保通过企业总线互连的业务流程间的消息的正确交付，还包括基于内容的路由功能。
  
  
    3)中介: 提供位置透明的路由和定位服务；提供多种消息传递形式；支持广泛使用的传输协议。
  
  
    4)多服务集成方式:  如JCA，Web服务，Messaging ，Adaptor等.
  
  
    5)服务和事件管理支持:  调用服务的记录、测量和监控数据；提供事件检测、触发和分布功能；
  
  
    二、ESB的八个扩展功能: 
  
  
    1) 面向服务的元数据管理:  他必须了解被他中介的两端,即服务的请求以及请求者对服务的要求，以及服务的提供者和他所提供的服务的描述；
  
  
    2) Mediation : 它必须具有某种机制能够完成中介的作用，如协议转换；
  
  
    3) 通信: 服务发布、订阅，响应 请求，同步异步消息，路由和寻址等；
  
  
    4) 集成:  遗留系统适配器，服务编排和映射，协议转换，数据变换，企业应用集成中间件的连续等。
  
  
    5) 服务交互:  服务接口定义，服务实现的置换，服务消息模型，服务目录和发现等。
  
  
    6) 服务安全:  认证和授权、不可否认和机密性、安全标准的支持等；
  
  
    7) 服务质量:  事务，服务的可交付性等；
  
  
    8) 服务等级:  性能、可用性等。
  
  
    ESB 中最常提到的两个功能是消息转换和消息路由。
  
  
    三、ESB架构
  
  
    ESB 是传统中间件技术与XML、Web服务等技术相互结合的产物，ESB的出现改变了传统的软件架构，可以提供比传统中间件产品更为廉价的解决方案，同时它还可以消除不同应用之间的技术差异，让不同的应用服务器协调运作，实现了不同服务之间的通信与整合。从功能上看，ESB提供了事件驱动和文档导向的处理模式，以及分布式的运行管理机制，它支持基于内容的路由和过滤，具备了复杂数据的传输能力，并可以提供一系列的标准接口。
  
  
    四、ESB的应用特征
  
  
    大规模分布式的企业应用需要相对简单而实用的中间件技术来简化和统一越来越复杂、繁琐的企业级信息系统平台。面向服务体系架构（SOA) 是能够将应用程序的不同功能单元通过服务之间定义良好的接口和契约联系起来。SOA使用户可以不受限制地重复使用软件、把各种资源互连起来，只要IT人员选用标准接口包装旧的应用程序、把新的应用程序构建成服务，那么其他应用系统就可以很方便的使用这些功能服务。
  
  
    支撑SOA的关键是其消息传递架构-企业服务总线（ESB) 。ESB是传统中间件技术与XML、Web服务等技术相互结合的产物，用于实现企业应用不同消息和信息的准确、高效和安全传递。ESB的出现改变了传统的软件架构，可以提供比传统中间件产品更为廉价的解决方案，同时它还可以消除不同应用之间的技术差异，让不同的应用服务协调运作，实现不同服务之间的通信与整合。ESB在不同领域具有非常广泛的用途:
  
  
    电信领域: ESB能够在全方位支持电信行业OSS的应用整合概念。是理想的电信级应用软件承载平台。
  
  
    电力领域: ESB能够在全方位支持电力行业EMS的数据整合概念，是理想的SCADA系统数据交换平台。
  
  
    金融领域: ESB能够在全方位支持银企间业务处理平台的流程整合概念，是理想的B2B交易支撑平台。
  
  
    电子政务: ESB能够在全方位支持电子政务应用软件业务基础平台、信息共享交换平台、决策分析支撑平台和政务门户的平台化实现。
  
  
    五、几种ESB的结构
  
  
    ESB提供了一种开放的、基于标准的消息机制，通过简单的标准适配器和接口，来完成粗粒度应用（服务) 和其他组件之间的互操作，能够满足大型异构企业环境的集成需求。它可以在不改变现有基础结构的情况下让几代技术实现互操作。
  
  
    通过使用ESB，可以在几乎不更改代码的情况下，以一种无缝的非侵入方式使企业已有的系统具有全新的服务接口，并能够在部署环境中支持任何标准。更重要的是，充当"缓冲器"的ESB（负责在诸多服务之间转换业务逻辑和数据格式) 与服务逻辑相分离，从而使得不同的应用程序可以同时使用同一服务，用不着在应用程序或者数据发生变化时，改动服务代码。
  
  
    1. IBM WebSphere ESB
  
  
    IBM 提供了三种 ESB 产品: IBM WebSphere ESB、IBM WebSphere Message Broker、IBM WebSphere DataPower Integration Appliance XI50。根据您的需求选择 ESB 来增强您的 SOA。WebSphere ESB 是一种基于平台的 ESB，作为集成的 SOA 平台，针对 WebSphere 应用服务器进行了优化。WebSphere Message Broker 是跨平台的 ESB，是为异构 IT 环境中的统一连接和转换而构建的。WebSphere DataPower Integration Appliance XI50 是一种基于设备的 ESB，是为简化的部署和更强的安全性而构建的。客户面临着从简单到复杂的各式各样的 ESB 需求。WebSphere ESB的结构如图一所示。
  
  
    1. Microsoft ESB
  
  
    微软通过其应用平台提供了全面的ESB服务，包括: Windows Server 2003,.NET Framework, BizTalk&reg;Server 2006 R2. 应用平台提供了一个基础架构，基于此可以灵活和安全地重复使用架构和商业服务，并具有协调原有的服务整合到新的端到端的业务流程中的能力。
  
  
    微软通过一些列的产品Windows Server 2003, the .NET Framework 3.0, and BizTalk Server 2006作为对企业实现ESB的支撑,Microsoft ESB Guidance是基于BizTalk Server 2006一组应用，它提供以下公用的ESB组件: l Message routing (消息路由) l Message validation (消息验证) l Message transformation (消息转换) l Centralized exception management(集中的异常管理) l Extensible adapter framework(可扩展的适配器框架) l Service orchestration(服务的编制支持) l Business rules engine(业务规则引擎) l Business activity monitoring(业务活动监视)微软 ESB 指南提供了架构指导，模式和实践，以及一套BizTalk Server 和 .NET Framework 组件来简化基于微软平台的大型或小规模的ESB解决方案的开发。它还可以帮助开发人员扩展现有的信息和集成解决方案，包括的一些服务和组件。
  
  
    1. JBOSS SOA Platform
  
  
    JBoss Enterprise SOA Platform提供了一个基于标准的平台，用以集成应用、SOA服务、业务事件和自动化业务流程。这一SOA平台集成了特定版本的JBoss ESB、jBPM、Drools、和已得到验证的JBoss企业应用平台，把它们组织在一起形成一个单一的企业级发布。JBoss Enterprise SOA Platform打包了不少流行组件如: 
  
  
    l JBoss ESB l JBoss jBPM jPDL l JBoss Rules (Drools) l JBoss Application Server l Hibernate l Hibernate Entity Manager l Hibernate Annotations l JBoss Seam l JBoss Web (嵌入式Tomcat 6.0) l JBoss Cache l JGroups l JBoss Messaging l JBoss Transactions l JBoss Web Services (JBossWS) l JBossXB l JBoss AOP l JBoss Remoting l JBoss Serialization l JacORB4. ServiceMix对ESB的实现
  
  
    ServiceMix是一个建立在JBI (JSR 208)语法规则和APIs上的开源ESB(Enterprise Service Bus:企业服务总线)项目。ServiceMix是基于JBI的ESB。它是开源的基于JBI语义和API的ESB和SOA工具包，以Apache许可证方式发布。 它是轻量的ESB实现，易于作为嵌入式ESB使用;集成了对Spring技术的支持;可以在客户端或服务器端运行;可以作为独立的ESB提供者，也可以作为另外ESB的服务组件; 可以在JavaSE或JavaEE服务器中使用；ServiceMix同Apache Geronimo以及JBoss服务器完全集成，并且在Apache Geronimo服务器中可以直接部署JBI组件和服务。Java Business Integration (JBI,Java业务集成)技术规范定义了SOA的服务导向集成的内核和组成架构。它对公共讯息路径架构、服务引擎与捆绑的插件程序接口，以及复合型服务描述机制等都进行了标准化，这样就将多种服务结合成为一个单一的可执行的和可审核的工作单元。JBI和ServiceMix关系图JBI并不是一个为开发者设计的一个接口，更准确的说它是在JBI容器里为集成商提供相互集成的一个体系和一系列的接口。所以人们能集合他们所需要的所有部分，做出一个总体解决。例如在理论你能从BPEL引擎上，EJB容器上或者是数据传输产品上集合一个基础设施，并且能够集成的很合适。 ServiceMix 中包含完整的JBI容器，支持JBI规范的所有功能要求:l 规范化消息服务和路由 l JBI管理Beans (MBeans)l 组件管理和安装的Ant任务l 对JBI部署单元的完全支持，支持JBI组件的热部署
  
  
    5.WebOTX ESB
  
  
    WebOTX Enterprise Service Bus（以下简称WebOTX ESB) 是灵活地结合基于SOA 的系统上的业务应用的，具有消息交换功能的服务运行平台的中间件，是在WebOTX Application Server 的Java EE 环境上动作的ESB 运行环境。WebOTX ESB 处于处理层和服务层中间的Hub产品的位置，使业务变更时系统能灵活对应。
  
  
    WebOTX ESB 遵循JBI1.0（服务总线的Java 标准定义) ，提供标准的对应了各种协议的组件，能实现与业务应用的无缝连接。此外，提供了丰富的适配器群以致能与大型计算机上的业务应用、EAI 工具等连接。而且，提供了能吸收服务间消息差异的高速XML 变换引擎，使得不进行任何变更就能灵活地实现系统的构筑。
  
  
    6.RES Infomatic Service Bu
  
  
    RES Infomatic Service Bus是锐易特软件信息整合解决方案中最为核心的企业级信息服务总线产品。该产品理念与核心技术跟IBM、Oracle等国际主流厂商的ESB产品同步，自2004年至今，经过了为期两年的国外产品原型设计和四年的国内本土研发与多行业重量级客户实践检验。广泛应用于金融、电信、政府、公共卫生等行业。它是由七款子产品构成的产品家族，包含了Universal Adapters 通用适配器、Message Broker消息代理、Service Monitor服务监控中心、Service Proxy 服务代理、Registry and Repository 服务资源注册中心、Configuration Manager 配置管理中心、Integration Tools 整合开发工具集，这些子产品相互支撑、协同工作，共同构成分布式信息服务总线的开发、部署、运行、管理的SOA全生命周期支持。
  
  
    7.Smart Service Bu
  
  
    Smart Enterprise Service Bus™是神州数码秉承SOA理念，结合十数年企业应用集成领域的最佳实践，研发的一套功能完善、高效稳定、灵巧开放的企业服务总线中间件。作为核心的交换平台，能保证7*24小时永不间断提供服务。提供最优的扩容方式，保证扩展线性度达到100%，为组织提供高吞吐量的优质基础服务。提供灵活的部署方式，支持集中部署、分布式部署及总分结构部署。最佳的IT架构治理平台，提供基于元数据的服务治理工具和系统监控工具套件。
  