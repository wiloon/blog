+++
date = 2020-05-15T10:48:07Z
title = "jul>slf4j>log4j2"

+++
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>jul-to-slf4j</artifactId>
        <version>1.7.25</version>
    </dependency>
    
    // Optionally remove existing handlers attached to j.u.l root logger
     SLF4JBridgeHandler.removeHandlersForRootLogger();  // (since SLF4J 1.6.5)
    
     // add SLF4JBridgeHandler to j.u.l's root logger, should be done once during
     // the initialization phase of your application
     SLF4JBridgeHandler.install();
     
     https://github.com/influxdata/influxdb-java/issues/443