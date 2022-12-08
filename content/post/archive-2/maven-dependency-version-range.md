---
title: maven dependency version range
author: "-"
date: 2017-02-08T08:30:48+00:00
url: /?p=9758
categories:
  - Inbox
tags:
  - reprint
---
## maven dependency version range

<http://maven.apache.org/components/enforcer/enforcer-rules/versionRanges.html>

## Version Range Specification

The [RequireMavenVersion][1] and [RequireJavaVersion][2] rules use the [standard Maven version range syntax][3]{.externalLink} with one minor change for ease of use (denoted with *):

      Range
    
    
    
      Meaning
    
  
  
  
    
      1.0
    
    
    
      x >= 1.0 * The default Maven meaning for 1.0 is everything (,) but with 1.0 recommended. Obviously this doesn't work for enforcing versions here, so it has been redefined as a minimum version.
    
  
  
  
    
      (,1.0]
    
    
    
      x <= 1.0
    
  
  
  
    
      (,1.0)
    
    
    
      x < 1.0
    
  
  
  
    
      [1.0]
    
    
    
      x == 1.0
    
  
  
  
    
      [1.0,)
    
    
    
      x >= 1.0
    
  
  
  
    
      (1.0,)
    
    
    
      x > 1.0
    
  
  
  
    
      (1.0,2.0)
    
    
    
      1.0 < x < 2.0
    
  
  
  
    
      [1.0,2.0]
    
    
    
      1.0 <= x <= 2.0
    
  
  
  
    
      (,1.0],[1.2,)
    
    
    
      x <= 1.0 or x >= 1.2. Multiple sets are comma-separated
    
  
  
  
    
      (,1.1),(1.1,)
    
    
    
      x != 1.1

<http://maven.apache.org/components/enforcer/enforcer-rules/requireMavenVersion.html>  
<http://maven.apache.org/components/enforcer/enforcer-rules/requireJavaVersion.html>  
<http://docs.codehaus.org/display/MAVEN/Dependency+Mediation+and+Conflict+Resolution#DependencyMediationandConflictResolution-DependencyVersionRanges>  
