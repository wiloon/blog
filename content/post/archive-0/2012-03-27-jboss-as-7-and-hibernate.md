---
title: JBoss AS 7 and Hibernate
author: "-"
type: post
date: 2012-03-27T02:54:15+00:00
url: /?p=2639
categories:
  - Development
  - Java
tags:
  - Jboss

---
JBoss AS 7 and Hibernate: what's up?

You might have heard the news: JBoss AS 7 is out 🙂 What does it mean from an Hibernate user perspective?

Before we go that way and if you are in a hurry Pete has written a few getting started guides covering JPA in JBoss AS 7. You might be interested.

Back to the subject: JBoss AS 7 and Hibernate.

Hibernate Core

First of all, JBoss AS 7 comes with Hibernate Core 4. This essentially means that AS 7 will be using the new foundational grounds for Hibernate Core. Hibernate Core 4 comes with many internal changes:

A new ServiceRegistry interface: many pieces of Hibernate are now service based and many contracts have been enhanced (like connections and second level caches)
  
A MetadataSources interface: instead of mixing configuration and mapping like the Configuration class was doing, we have now split the concerns and lifecycles
  
A package refactoring splitting classes into api, spi and internals: if your application depends on internals, you know you might get burnt by a minor/micro update
  
A new class loader service (see below)
  
Better logging with consistent error id (our goal is to build an error-id to solution database somewhere over time)
  
A move to Git and GitHub for version control: hopefully this is speeding up community contribution integration
  
Multi-tenancy

We have also introduced some new features, the most interesting definitely being multi-tenancy (see also here).

New classloader service

Why?

Historically, Hibernate relied on standard class-loading paradigms that targeted JSE and JEE deployment environments. However, with the growth of OSGi and other modular systems like JBoss AS 7, those same approaches no longer always work. So Hibernate needed a new approach that would allow it operate in all possible deployment environments.

How?

In Hibernate 4 we leverage the ServiceRegistry to define a pluggable service for providing interaction with the class-loading of the semantics of the environment in which Hibernate will be run. Specifically, the idea is to allow external entities (the user, the environment developers, etc) to define and plug in a custom scheme for class path interactions. For example, an OSGi container could choose to provide Hibernate (either directly or as its JPA provider) and install a custom service for class loader interactions to override the default one.

Hibernate Core in AS 7

JBoss AS 7 integrates with Hibernate 4.0.0.Beta1, to provide both the EE container managed JPA features and application managed access as well. The AS7 JPA subsystem integrates with Hibernate via the JPA specification SPI interfaces. In earlier releases of JBoss AS, JPA integration code was part of the EJB3 container (reflecting the evolution from EJB entity beans). Moving the JPA integration code into its own subsystem helps simplify the code and makes it easier to make changes.

Quick second-level cache tip

Enabling the (Infinispan) second level cache should be as simple as including the following in your persistence.xml file:

ENABLE_SELECTIVE
  
I (aka Scott Marlow) would like to thank the following people for contributing to the JBoss AS7 JPA subsystem:

Stuart Douglas for contributing to the JPA subsystem.
  
Steve Ebersole for contributing to the JPA subsystem (especially Hibernate 4.0 integration).
  
Jaikiran Pai for contributing to the JPA subsystem and answering an amazing number of questions in the forums (JPA + hundreds of other topics).
  
Emmanuel Bernard for answering my never ending JPA 2.0 specification questions.
  
Carlo de Wolf for answering my questions about the EJB3 subsystem (which the new code is based on).
  
What is next

Improving support for applications that use a different version of Hibernate than is packaged with JBoss AS 7. The plan is to let users deploy the Hibernate jars as well as a hibernate-jbossas7 integration jar. The integration jar will be tailored to the specific couple of Hibernate / JBoss AS version (or families of).

To be clear, Hibernate native applications can already include their own version of Hibernate in JBoss AS 7 simply by including the jar in their deployment. But we want JPA applications to benefit from this enhancement as well. Because it involves specification classes, this requires a bit more work.

We will also include additional tuning options to disable some of the JPA integration (ie prevent the container from starting the persistence unit).

Hibernate Validator and Bean Validation

What's new in AS7 in relation to Bean Validation? The short answer - nothing. It was already awesome 😉 The initial version - AS 7.0 - ships with Hibernate Validator 4.1.0.Final. This is the same Validator version as in AS 6 so no change there.

The long answer is that Hibernate Validator 4.2.0.Final merely missed the AS 7.0 release train and an upgrade is planned at the latest in AS 7.1. What will the update mean for AS users? Besides the usual bug fixes and performance improvements, the biggest new feature is the implementation of appendix C of the Bean Validation specification: method level validation.

With this API a design by contract approach is possible which can already be seen in action in the Seam Validation module. Another new feature is the ability to combine the composing constraints with AND and OR operators. There is also a fail fast mode in which validation stops on the first validation error and a new message interpolator which is able to interpolate the validated value.

As you can see AS 7.0 is just the beginning. More is to come in the coming releases...

Hibernate Search

We are working on Hibernate Search 4 which will be compatible with Hibernate Core 4. As a matter of fact, we have already published a compatible version via a Maven SNAPSHOT but expect a first alpha release soon.

Hibernate Search 4 is our chance to fix mistakes from the past. To be honest, the codebase and concepts have aged quite well despite the massive feature shifts we have done in Hibernate Search. Anyways, we are doing some changes including splitting API/SPI/implementations to help people discover when they use a class that is subject to change.

We are also working on a new per index manager to better use some of the new features and design changes of Lucene. This will give you more flexibility on how to index data on a per entity level (sync/async etc).

And remember, go try the blazingly fast, lightweight, modular, hot and incremental deployable, elegantly administrable, domain manageable, first class best of breed JBoss Application Server 7

Happy code/fast deploy/test cycles 🙂

Steve, Hardy, Scott Marlow and Emmanuel